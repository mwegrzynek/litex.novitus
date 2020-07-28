from litex.novitus import unpack_flags, assemble_packet, nmb, parse_cash_register_data_reply


def test_unpack_flags():
    assert unpack_flags(b'm') == [True, False, True, True, False, True, True, False]


def test_assemble_packet_crc():
    assert assemble_packet(
        command='#i',
        parameters=['0'],
        texts=['100/']
    ) == b'\x1b\x50\x30\x23\x69\x31\x30\x30\x2f\x39\x42\x1b\x5c'


def test_parse_cash_register_data_reply():
    assert 'PTU_A' in parse_cash_register_data_reply(
        b'2#X0;1;0;1;1;0;20;07;23/23.00/08.00/05.00/00.00/100.00/101.00/101.00/169/810.19/0.00/0.00/0.00/0.00/0.00/0.00/0.00/ABC1234567890F1'
    )