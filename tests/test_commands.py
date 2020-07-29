
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


def test_invoice_begin_cancel(printer):

    printer.invoice_begin(
        no_of_lines=1,
        customer='Litex Service Sp. z o.o.',
        invoice_type='invoice',
        number='1/TEST/2020',
        nip='6220006775'
    )

    printer.invoice_cancel()


def test_invoice_cancel_with_no_active_invoice(printer):
    # Works even without open transaction
    printer.invoice_cancel()


def test_double_invoice_begin(printer):
    printer.invoice_begin(
        no_of_lines=1,
        customer='Litex Service Sp. z o.o.',
        nip='6220006775',
        number='FAILED/1/2020'
    )

    with pytest.raises(ProtocolError):
        printer.invoice_begin(
            no_of_lines=1,
            customer='Litex Service Sp. z o.o.',
            nip='6220006775',
            number='FAILED/2/2020'
        )

    printer.invoice_cancel()


@pytest.mark.paper
def test_single_position_invoice(printer):
    printer.set_error('silent')
    printer.invoice_cancel()

    printer.invoice_begin(
        no_of_lines=1,
        customer=(
            'Litex Service Sp. z o.o.\n'
            'ul. Staroprzygodzka 117\n'
            '63-400 Ostrów Wielkopolski\n'
            'Poland'
        ),
        nip='6220006775',
        number='FV 1/2020'
    )
    printer.item(
        lineno=1,
        name='Test ąśćłóśź',
        quantity=10,
        ptu='A',
        price=10
    )
    printer.invoice_close(
        100,  
        buyer='John Doe',
        seller='Jane Doe'
    )

@pytest.mark.paper
def test_multiple_position_invoice_with_discount(printer):
    printer.set_error('silent')
    printer.invoice_cancel()

    printer.invoice_begin(
        no_of_lines=2,
        number='FV 2/2020',
        invoice_type='invoice',        
        customer=(
            'Litex Service Sp. z o.o.\n'
            'ul. Staroprzygodzka 117\n'
            '63-400 Ostrów Wielkopolski\n'
            'Poland'
        ),
        nip='PL6220006775'        
    )
    printer.item(
        lineno=1,
        name='Test ąśćłóśź',
        quantity=10,
        ptu='A',
        price=10,
        discount_name='Promotion',
        discount_value='10%',
        discount_descid=2
    )
    printer.item(
        lineno=2,
        name='Test zażółć gęślą jaźń',
        quantity=15,        
        description='A long description',
        ptu='A',
        price=5
    )
    # printer.discount(
    #     value='10%',
    #     name='Seasonal'
    # )
    printer.invoice_close(
        165.0,
        #discount=10,  
        buyer='John Doe',
        seller='Jane Doe'
    )


@pytest.mark.paper
def test_multiple_position_receipt_with_discount(printer):
    printer.set_error('silent')
    printer.receipt_cancel()
    printer.receipt_begin(
        buyer_identifier='6220006775',
        system_identifier='1/10/2020',
        additional_lines=[            
            'Second line',
            'Third line'
        ]
    )
    printer.item(
        lineno=1,
        name='Test next',
        quantity=2,        
        ptu='A',
        price=4
    )
    printer.item(
        lineno=2,
        name='Test zażółć gęślą jaźń 2',
        quantity=4,        
        description='A long description',
        ptu='A',
        price=2
    )
    printer.discount(
        value='20%',
        name='Employee discount'
    )
    printer.receipt_close(
        16.0,
        'John Doe',
        discount=20,
        cash=20.00
    )

@pytest.mark.paper
def test_multiple_item_receipt_with_item_discount(printer):
    printer.set_error('silent')
    printer.receipt_cancel()
    printer.receipt_begin(
        buyer_identifier='6220006775',
        system_identifier='2/TEST/2020',  
    )
    printer.item(
        lineno=1,
        name='Test discount',
        quantity=2,
        ptu='A',
        price=4,
        discount_name='Promotion',
        discount_value='10%',
        discount_descid=2
    )
    printer.item(
        lineno=2,
        name='Test zażółć gęślą jaźń 2',
        quantity=4,
        description='A long description',
        ptu='A',
        price=2
    )
    printer.discount(
        value='20%',
        name='Employee'
    )
    printer.receipt_close(
        15.20,        
        'John Doe',
        discount=20.0,
        cash=50.0
    )

@pytest.mark.paper
def test_multiple_item_receipt_with_item_discount_and_payment(printer):
    printer.set_error('silent')
    printer.receipt_cancel()

    printer.receipt_begin(
        system_identifier='3/TEST/2020',  
    )
    printer.item(
        lineno=1,
        name='Test discount',
        quantity=2,
        ptu='A',
        price=4,
        discount_name='Promotion',
        discount_value='10%',
        discount_descid=2
    )
    printer.item(
        lineno=2,
        name='Test zażółć gęślą jaźń 2',
        quantity=4,        
        description='A long description',
        ptu='A',
        price=2
    )
    printer.discount(
        value='20%',
        name='Employee'
    )
    printer.payment_add(
        'card',
        value=11.0
    )
    printer.payment_add(
        'cash',
        value=1.16
    )
    printer.receipt_close(
        15.20,        
        'John Doe',
        discount=20
    )


def test_open_drawer(printer):
    printer.open_drawer()


def test_taxrates_get(printer):
    res = printer.taxrates_get()
    assert res[0] == ('A', '23.00%')
    assert res[1] == ('B', '8.00%')
    assert res[4] == ('E', 'free')