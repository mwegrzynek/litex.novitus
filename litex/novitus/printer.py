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

    # def invoice_begin(self, **kwargs):

    #     defined_args = dict(
    #         invoice_type=('invoice', 'pharmacy'),
    #         number=None,
    #         nip=None,
    #         description=('both', 'original'),
    #         paymentname=None,
    #         paymentdate=None,
    #         recipient=None,
    #         issuer=None,
    #         copies=None,
    #         margins=('yes', 'no'),
    #         signarea=('yes', 'no'),
    #         customernameoptions=('info', 'all', 'none'),
    #         sellernameoptions=('info', 'all', 'none'),
    #         paidlabel=None,
    #         selldate=None,
    #         buyerlabel=None,
    #         additionalinfo=None
    #     )

    #     cmd = E.invoice()

    #     cmd.set('action', 'begin')

    #     # Prepare options
    #     options = set(kwargs.pop('options', []))
    #     if options:
    #         for op in options:
    #             if op in range(1, 20):
    #                 op_tag = cmd.append(E.option('', id=str(op)))

    #     # Prepare customer info
    #     customer = kwargs.pop('customer', None)
    #     if customer:
    #         cust_tag = cmd.append(E.customer(customer))

    #     args = {}
    #     for name, value in kwargs.items():
    #         if name not in defined_args:
    #             raise TypeError('Unknown argument: {}'.format(name))

    #         allowed_values = defined_args.get(name)
    #         if allowed_values is not None and value not in allowed_values:
    #             raise TypeError(
    #                 'Argument {} has wrong value: {} (not in {})'.format(
    #                     name,
    #                     value,
    #                     allowed_values
    #                 )
    #             )

    #         if value is not None:
    #             cmd.set(name, str(value))

    #     self.send_command(cmd, check_for_errors=True)

    # def invoice_cancel(self):
    #     cmd = E.invoice('', action='cancel')
    #     self.send_command(cmd, check_for_errors=True)

    # def invoice_close(
    #     self,
    #     total,
    #     systemno,
    #     checkout,
    #     cashier,
    #     buyer
    # ):
    #     cmd = E.invoice(
    #         '',
    #         action='close',
    #         total=str(total),
    #         systemno=systemno,
    #         checkout=checkout,
    #         cashier=cashier,
    #         buyer=buyer
    #     )
    #     self.send_command(cmd, check_for_errors=True)

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
                '2;', 
                str(discount_descid)
            ]

            texts += [
                discount_value.strip('%'),
                '\r',
                discount_name,
                '\r'
            ]

        if description:
            params.append('1;')
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

    # def payment_add(
    #     self,
    #     type_,
    #     value,
    #     rate=1,
    #     mode='payment',
    #     name=''
    # ):
    #     cmd = E.payment(
    #         '',
    #         action='add',
    #         type=type_,
    #         value=str(value),
    #         rate=str(rate),
    #         mode=mode,
    #         name=name
    #     )

    #     self.send_command(cmd, check_for_errors=True)

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

    def receipt_cancel(self):    
        self.send_command(
            command='$e',
            parameters=['0'],
            check_for_errors=True
        )

    def receipt_close(
        self,
        total,        
        cashier,
        discount=0,
        cash=0
    ):                
        self.send_command(
            command='$e',
            parameters=['1;', str(discount)],
            texts=[
                cashier,
                '\r',
                nmb(cash),
                '/',
                nmb(total),
                '/'
            ],
            check_for_errors=True
        )

    def open_drawer(self):
        self.send_command(
            command='$d',
            parameters=['1']
        )

    # def info_checkout(self, type_='receipt'):

    #     cmd = E.info(
    #         '',
    #         action='checkout',
    #         type=type_,
    #         isfiscal='?',
    #         lasterror='?'
    #     )

    #     return self.send_command(
    #         cmd,
    #         read_reply=True,
    #     ).info



