def yn(val: bool) -> str:
    '''Protocol compatible bool format'''
    return 'yes' if val else 'no'


def nmb(val: float) -> str:
    '''Protocol compatible number format'''
    return '{:.2f}/'.format(val)


def checksum(txt: str) -> str:
    '''Packet checksum'''
    chk = 255
    for el in txt:
        chk ^= el

    return ('{:02x}'.format(chk)).upper().encode('UTF-8')


def unpack_flags(flags: bytes) -> list:
    return [flags[i//8] & 1 << i%8 != 0 for i in range(len(flags) * 8)]


def assemble_packet(
        command,
        parameters=tuple(),
        texts=tuple()
    ):
        pkt = b''.join(parameters)
        pkt += command

        for txt in texts:
            pkt += txt.encode('cp1250')

        return b'\x1bP' + pkt + checksum(pkt) + b'\x1b\\'
