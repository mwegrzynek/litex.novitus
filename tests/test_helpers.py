from litex.novitus import unpack_flags, assemble_packet


def test_unpack_flags():
    assert unpack_flags(b'm') == [True, False, True, True, False, True, True, False]


def test_assemble_packet_crc():
    assert assemble_packet(
        command='#i',
        parameters=(0,),
        texts=['100/']
    ) == b'\x1b\x50\x30\x23\x69\x31\x30\x30\x2f\x39\x42\x1b\x5c'
