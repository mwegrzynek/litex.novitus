# litex.novitus
## Driver for a Polish fiscal printer with Novitus protocol

**Fiscal printer** is a [fiscal memory device](https://en.wikipedia.org/wiki/Fiscal_memory_device) used to record retail sales in Poland and few other countries in the world (eg. Russia, Czechia).

This library implements parts of [**classic** Novitus protocol](https://www.novitus.pl/sites/default/files/dla-programistow/drukarki-fiskalne/protokol_komunikacyjny_novitus_1.09_ver_online.pdf) of one of the major Polish manufacturers [Novitus](https://www.novitus.pl/).

Printing receipt example (for more, see tests):

```python
from litex.novitus import Printer

# uses USB device autodetection and no checksumming by default
# for more url examples, see PySerial documentation
# https://pyserial.readthedocs.io/en/latest/url_handlers.html
printer = Printer(
    url='hwgrep://.*Novitus.*'
) 

printer.receipt_begin(
    system_identifier='1/2020' 
)

printer.item(
    line_no=1,
    name='First product',
    quantity=2,        
    ptu='A',
    price=4
)

printer.item(
    line_no=2,
    name='Second product',
    quantity=4,        
    description='A long description',
    ptu='A',
    price=2
)

printer.receipt_close(
    16.0,
    'John Doe'
)

```