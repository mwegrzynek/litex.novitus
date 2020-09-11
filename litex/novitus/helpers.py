import re


from . import mazovia
from .exceptions import ReplyNotImplemented


def yn(val: bool) -> str:
    '''Protocol compatible bool format'''
    return 'yes' if val else 'no'


def nmb(val: float) -> str:
    '''Protocol compatible number format'''
    return '{:.2f}'.format(val)


def checksum(txt: str, encoding='mazovia') -> str:
    '''Packet checksum'''
    chk = 255
    for el in txt:
        chk ^= el

    return ('{:02x}'.format(chk)).upper().encode(encoding)


def unpack_flags(flags: bytes) -> list:
    return [flags[i//8] & 1 << i%8 != 0 for i in range(len(flags) * 8)]


def assemble_packet(
        command,
        parameters=tuple(),
        texts=tuple(),
        encoding='mazovia'
    ):
        txt = ''.join(parameters)
        txt += command
        txt += ''.join(texts)

        pkt = txt.encode(encoding)

        return b'\x1bP' + pkt + checksum(pkt, encoding) + b'\x1b\\'


def parse_cash_register_data_reply(pkt):
    type_ = pkt[:3]

    reply = None

    if type_ == b'2#X':
        reply = re.match(
            b'^(?P<lastcommanderror>[01]);(?P<fiscal>[01]);(?P<intransaction>[01]);'
            b'(?P<lasttransactionerror>[01]);1;(?P<zeroingcount>\d+);(?P<year>\d{1,2});'
            b'(?P<month>\d{1,2});(?P<day>\d{1,2})/(?P<PTU_A>[\d.]+)/(?P<PTU_B>[\d.]+)/'
            b'(?P<PTU_C>[\d.]+)/(?P<PTU_D>[\d.]+)/(?P<PTU_E>[\d.]+)/(?P<PTU_F>[\d.]+)/'
            b'(?P<PTU_G>[\d.]+)/(?P<receiptcount>\d+)/(?P<TOT_A>[\d.]+)/(?P<TOT_B>[\d.]+)/'
            b'(?P<TOT_C>[\d.]+)/(?P<TOT_D>[\d.]+)/(?P<TOT_E>[\d.]+)/(?P<TOT_F>[\d.]+)/(?P<TOT_G>[\d.]+)/'
            b'(?P<cash>[\d.]+)/(?P<serialno>.*)',
            pkt[3:-2]
        ).groupdict()
    else:
        raise ReplyNotImplemented

    return reply


def parse_ptu_percentages(val, encoding='mazovia'):
    ret = val.lstrip(b'0').decode(encoding) + '%'

    if ret == '100.00%':
        ret = 'free'
    elif ret == '101.00%':
        ret = 'unused'

    return ret

