
import pytest


from litex.novitus.exceptions import CommunicationError, ProtocolError


def test_dle(printer):
    assert printer.dle()['online'] in ('yes', 'no')

def test_enq(printer):
    assert printer.enq()['fiscal'] in ('yes', 'no')


def test_bel(printer):
    assert printer.bel() is None


def test_can(printer):
    assert printer.can() is None


def test_set_error(printer):
    assert printer.set_error('silent') is None


def test_get_error(printer):
    assert printer.get_error() == 0


def test_cash_register_data(printer):
    res = printer.cash_register_data(mode=22)
    assert 'serialno' in res


# def test_invoice_begin_cancel(printer):

#     printer.invoice_begin(
#         invoice_type='invoice',
#         number='1/TEST/2020',
#         nip='6220006775'
#     )

#     printer.invoice_cancel()


# def test_invoice_cancel_with_no_active_invoice(printer):
#     # Works even without open transaction
#     printer.invoice_cancel()


# def test_double_invoice_begin(printer):
#     printer.invoice_begin(invoice_type='invoice')

#     with pytest.raises(ProtocolError):
#         printer.invoice_begin(invoice_type='invoice')

#     printer.invoice_cancel()


# @pytest.mark.paper
# def test_single_position_invoice(printer):
#     printer.invoice_begin(invoice_type='invoice', copies=-1)
#     printer.item(
#         name='Test ąśćłóśź',
#         quantity=10,
#         quantityunit='pcs',
#         ptu='A',
#         price=10
#     )
#     printer.invoice_close(
#         100,
#         '@1/TEST/2020',
#         '10',
#         'John Doe',
#         'Jane Doe'
#     )

# @pytest.mark.paper
# def test_multiple_position_invoice_with_discount(printer):
#     printer.invoice_begin(
#         invoice_type='invoice',
#         copies=-1,
#         description='original',
#         customer='Litex Service Sp. z o.o.',
#         nip='PL6220006775',
#         options=set([3, 4, 5, 6]),
#         customernameoptions='info',
#         sellernameoptions='none',
#         signarea='no'
#     )
#     printer.item(
#         name='Test ąśćłóśź',
#         quantity=10,
#         quantityunit='pcs',
#         ptu='A',
#         price=10
#     )
#     printer.item(
#         name='Test zażółć gęślą jaźń',
#         quantity=15,
#         quantityunit='pcs',
#         description='A long description',
#         ptu='A',
#         price=5def test_taxrates_get(printer):
#     res = printer.taxrates_get()
#     assert res[0] == ('A', '23.00%')
#     assert res[1] == ('B', '8.00%')
#     assert res[4] == ('E', 'free')
#     )
#     printer.discount(
#         value='10%',
#         name='Seasonal',
#         descid=12
#     )
#     printer.invoice_close(
#         157.5,
#         '@1/TEST/2020',
#         '10',
#         'John Doe',
#         'Jane Doe'
#     )


# @pytest.mark.paper
# def test_multiple_position_receipt_with_discount(printer):
#     printer.receipt_begin()
#     printer.item(
#         name='Test next',
#         quantity=2,
#         quantityunit='pcs',
#         ptu='A',
#         price=4
#     )
#     printer.item(
#         name='Test zażółć gęślą jaźń 2',
#         quantity=4,
#         quantityunit='pcs',
#         description='A long description',
#         ptu='A',
#         price=2
#     )
#     printer.discount(
#         value='20%',
#         name='Employee',
#         descid=7
#     )
#     printer.receipt_close(
#         12.8,
#         '2/TEST/2020',
#         '10',
#         'John Doe',
#         nip='6220006775'
#     )

# @pytest.mark.paper
# def test_multiple_item_receipt_with_item_discount(printer):
#     printer.receipt_begin()
#     printer.item(
#         name='Test discount',
#         quantity=2,
#         quantityunit='pcs',
#         ptu='A',
#         price=4,
#         discount_name='Promotion',
#         discount_value='10%',
#         discount_descid=1
#     )
#     printer.item(
#         name='Test zażółć gęślą jaźń 2',
#         quantity=4,
#         quantityunit='pcs',
#         description='A long description',
#         ptu='A',
#         price=2
#     )
#     printer.discount(
#         value='20%',
#         name='Employee',
#         descid=7
#     )
#     printer.receipt_close(
#         12.16,
#         '2/TEST/2020',
#         '10',
#         'John Doe',
#         nip='6220006775'
#     )

# @pytest.mark.paper
# def test_multiple_item_receipt_with_item_discount_and_payment(printer):
#     printer.receipt_begin()
#     printer.item(
#         name='Test discount',
#         quantity=2,
#         quantityunit='pcs',
#         ptu='A',
#         price=4,
#         discount_name='Promotion',
#         discount_value='10%',
#         discount_descid=1
#     )
#     printer.item(
#         name='Test zażółć gęślą jaźń 2',
#         quantity=4,
#         quantityunit='pcs',
#         description='A long description',
#         ptu='A',
#         price=2
#     )
#     printer.discount(
#         value='20%',
#         name='Employee',
#         descid=7
#     )
#     printer.payment_add(
#         'card',
#         value=11.0
#     )
#     printer.payment_add(
#         'cash',
#         value=1.16
#     )
#     printer.receipt_close(
#         12.16,
#         '2/TEST/2020',
#         '10',
#         'John Doe',
#         nip='6220006775'
#     )


def test_open_drawer(printer):
    printer.open_drawer()


# def test_info_checkout(printer):
#     res = printer.info_checkout()
#     assert res.get('isfiscal') == 'yes'
#     assert res.get('lasterror') == '0'
#     assert res.ptu.get('name') == 'A'
#     assert res.ptu.text


def test_taxrates_get(printer):
    res = printer.taxrates_get()
    assert res[0] == ('A', '23.00%')
    assert res[1] == ('B', '8.00%')
    assert res[4] == ('E', 'free')