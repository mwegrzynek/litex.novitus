'''
Novitus Protocol implementation
'''
import logging
import time
import enum


import serial


from .helpers import assemble_packet, unpack_flags, yn, parse_cash_register_data_reply, parse_ptu_percentages, nmb
from .exceptions import CommunicationError, ProtocolError


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


ERROR_HANDLING = {
    'display': '0',
    'silent': '1',
    'autowithdisplay': '2',
    'autowithoutdisplay': '3'
}


BUYER_IDENTIFIER = {
    'NIP': '1',
    'REGON': '2',
    'PESEL': '3'
}

PAYMENT_TYPES = {
    'cash': '0',
    'card': '1',
    'cheque': '2',
    'bon': '3',
    'other': '4',
    'credit': '5',
    'account': '6',
    'foreign': '7',
    'transfer': '8',
    'mobile': '9',
    'voucher': '10'
}


class Printer:

    def __init__(self, url, timeout=10, encoding='cp1250'):
        self.url = url
        self.timeout = timeout
        self.encoding = encoding
        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self._conn = serial.serial_for_url(self.url)
            self._conn.timeout = self.timeout

        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def send_command(
        self,
        command,
        parameters=tuple(),
        texts=tuple(),
        read_reply=False,
        check_for_errors=False
    ):
        pkt = assemble_packet(command, parameters, texts, self.encoding)

        log.debug('Sending command: %s', pkt)
        self.conn.write(pkt)

        if read_reply:
            reply = self.conn.read_until(b'\x1b\\', 5000)

            if not reply:
                raise CommunicationError('No reply from printer')

            log.debug('Received reply: %s', reply)
        else:
            reply = None

        if check_for_errors:
            time.sleep(0.1)
            err = self.get_error()
            if err != 0:
                raise ProtocolError(err)

        return reply

    def dle(self):
        self.conn.write(b'\x10')
        status = unpack_flags(self.conn.read())[:3]
        return {
            'online': yn(status[2]),
            'papererror': yn(status[1]),
            'printererror': yn(status[0])
        }

    def enq(self):
        self.conn.write(b'\x05')
        status = unpack_flags(self.conn.read())[:4]
        return {
            'fiscal': yn(status[3]),
            'lastcommanderror': yn(status[2]),
            'intransaction': yn(status[1]),
            'lasttransactioncorrect': yn(status[0])
        }

    def bel(self):
        self.conn.write(b'\x07')

    def can(self):
        self.conn.write(b'\x18')

    def set_error(self, value):

        self.send_command(
            command='#e',
            parameters=[ERROR_HANDLING[value]]
        )

    def get_error(self):
        reply = self.send_command(
            command='#n',
            read_reply=True
        )[5:-2]

        return int(reply)

    def cash_register_data(self, mode=21):
        reply = self.send_command(
            command='#s',
            parameters=[str(mode)],
            read_reply=True
        )[2:-2]

        return parse_cash_register_data_reply(reply)

    def taxrates_get(self):

        reply = self.cash_register_data(mode=22)

        tax_rates = [
            (key[-1], parse_ptu_percentages(val, self.encoding))
            for key, val in reply.items() if key.startswith('PTU_')
        ]

        return tax_rates

    def invoice_begin(
        self,
        no_of_lines,        
        customer,
        nip,
        number,
        invoice_type='invoice',
        signarea=True,
        copies=0,
        payment_date=None,
        margins=True,
        recipient=None,
        issuer=None
    ):
        customer_lines = customer.split('\n')

        params = [
            str(no_of_lines), # invoice lines number
            ';',
            str(len(customer_lines)), # customer lines number
            ';',
            '1' if invoice_type == 'invoice' else '2',
            ';',
            '2', # Oryginał / kopia
            ';',
            '1' if margins else '0', # upper margin
            ';',
            '0', # ignored
            ';',
            '255' if copies == 0 else str(copies - 1),
            ';',
            '0', # ignored
            ';',
            '0', # ignored
            ';',
            '0' if signarea else '1',
            ';',
            '0' # no country symbol before sellers NIP
        ]

        texts = [
            number,
            '\r',            
        ]

        for cl in customer_lines:
            texts += [
                cl,
                '\r'
            ]

        texts += [
            nip,
            '\r', 
            '\r', # payment date
            '\r'  # payment form
        ]

        if payment_date is not None:
            texts += [
                payment_date,
                '\r'
            ]

        if recipient is not None:
            texts += [
                recipient,
                '\r'
            ]

        if issuer is not None:
            texts += [
                issuer,
                '\r'
            ]

        texts += [
            '#',
            number,
            '\r',
            customer_lines[0],
            '\r'
        ]        

        self.send_command(
            command='$h',
            parameters=params,
            texts=texts,
            check_for_errors=True
        )

    def invoice_cancel(self):    
        self.send_command(
            command='$e',
            parameters=['0'],
            check_for_errors=True
        )

    def invoice_close(
        self,
        total,        
        discount=0,
        cash=0,
        paid_line='',
        buyer='',
        seller=''
    ):                
        self.send_command(
            command='$e',
            parameters=[
                '1;0;0;1;1;1;',
                '1' if paid_line else '0',
                ';',
                '0', # buyer name options
                ';',
                '0'  # seler name options
            ],
            texts=[
                paid_line,
                '\r',
                buyer,
                '\r',
                seller,
                '\r',                
                nmb(cash),
                '/',
                nmb(total),
                '/',
                nmb(discount),
                '/'
            ],
            check_for_errors=True
        )

    def item(
        self,
        lineno,    
        name,
        quantity,        
        ptu,
        price,
        plu='',        
        description='',
        discount_name='',
        discount_value=None,
        discount_descid=16
    ):
        params = [str(lineno)]
        texts = [name, '\r']

        if plu:
            texts += [plu, '\r']

        texts += [
            nmb(quantity),
            '\r',
            ptu,
            '/',
            nmb(price),
            '/',
            nmb(price * quantity),
            '/'
        ]

        if discount_value is not None:
            params += [
                ';',
                '2' if discount_value.endswith('%') else '1',
                ';', 
                str(discount_descid)
            ]

            texts += [
                discount_value.strip('%'),
                '/',
                discount_name,
                '\r'
            ]

        if description:
            if discount_value is None:
                params.append(';0;0')                

            params.append(';1')
            texts += [description, '\r']
        
        self.send_command(
            command='$l',
            parameters=params,
            texts=texts,
            check_for_errors=True
        )

    def discount(
        self,
        value,
        name
    ):
        discount_type = '1' if value.endswith('%') else '3'

        self.send_command(
            command='$n',
            parameters=[discount_type],
            texts=[
                name,
                '\r',
                value.strip('%'),
                '/'
            ],
            check_for_errors=True
        )

    def markup(
        self,
        value,
        name
    ):
        markup_type = '2' if value.endswith('%') else '4'

        self.send_command(
            command='$n',
            parameters=[markup_type],
            texts=[
                name,
                '\r',
                value.strip('%'),
                '/'
            ],
            check_for_errors=True
        )

    def payment_add(
        self,
        type_,
        value,
        mode='payment',
        name=''
    ):
        self.send_command(
            command='$b',
            parameters=[
                '1' if mode == 'payment' else '2',
                ';',
                PAYMENT_TYPES.get(type_, '4'), # set other, when nothing matches
            ],
            texts=[
                nmb(value),
                '/',
                name,
                '\r'
            ],
            check_for_errors=True
        )

    def receipt_begin(
        self,
        lines_count=0, # 0 - online
        system_identifier='',
        additional_lines=tuple(),
        buyer_identifier='',
        buyer_identifier_type='NIP'
    ):

        if system_identifier:
            additional_lines = [
                system_identifier
            ] + list(additional_lines)

        params = [
            str(lines_count),
            ';', 
            str(len(additional_lines))
        ]

        texts = [line + '\r' for line in additional_lines]

        if buyer_identifier:
            params += [
                ';0;',
                BUYER_IDENTIFIER[buyer_identifier_type],
                ';',
                '1'
            ]

            texts += [
                buyer_identifier,
                '\r'
            ]

        self.send_command(
            command='$h',
            parameters=params,
            texts=texts,
            check_for_errors=True
        )

    receipt_cancel = invoice_cancel

    def receipt_close(
        self,
        total,        
        cashier,
        discount=0,
        cash=0
    ):                
        self.send_command(
            command='$e',
            parameters=['1;0;0;1;1;1',],
            texts=[
                cashier,
                '\r',
                nmb(cash),
                '/',
                nmb(total),
                '/',
                nmb(discount),
                '/'
            ],
            check_for_errors=True
        )

    def open_drawer(self):
        self.send_command(
            command='$d',
            parameters=['1']
        )


