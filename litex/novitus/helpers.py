import zlib


def yn(val: bool) -> str:
    return 'yes' if val else 'no'
    

def unpack_flags(flags: bytes) -> list:     
    return [flags[i//8] & 1 << i%8 != 0 for i in range(len(flags) * 8)]


def crc32(txt: bytes) -> str:
    return hex(zlib.crc32(txt) & 0xffffffff)[2:].upper()


def assemble_packet(root, crc=False):    
    if crc:
        crc = crc32(etree_to_bytes(root))
        packet = obj.E.packet(root, crc=crc)
    else:
        packet = obj.E.packet(root)

    return packet
    
