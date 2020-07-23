from distutils.core import setup

version = '1.0.0'

install_requires = filter(
    lambda req: not req.startswith('-'),
    open('requirements.txt', 'r')
    .read()
    .split('\n')
)

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
    install_requires=install_requires
)
