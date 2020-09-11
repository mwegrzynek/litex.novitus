from os import path
from setuptools import setup

version = '1.0.1'


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='litex.novitus',
    version=version,
    description='A Novitus Protocol Fiscal Printer Library',
    author='Michał Węgrzynek',
    author_email='mwegrzynek@litexservice.pl',
    namespace_packages=['litex'],
    packages=[
        'litex.novitus'
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyserial'
    ]
)
