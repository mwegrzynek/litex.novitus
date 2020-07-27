from pprint import pprint


error_codes = {
    1: 'Nie zainicjowany zegar RTC',
    2: 'Nieprawidłowy bajt kontrolny',
    3: 'Nieprawidłowa ilość parametrów',
    4: 'Nieprawidłowy parametr',
    5: 'Błąd operacji z zegarem RTC',
    6: 'Błąd operacji z modułem fiskalnym',
    7: 'Nieprawidłowa data',
    8: 'Błąd operacji – niezerowe totalizery',
    9: 'Błąd operacji wejścia/wyjścia',
    11: 'Nieprawidłowa ilość stawek PTU',
    12: 'Nieprawidłowy nagłówek',
    13: 'Nie można refiskalizować urządzenia',
    15: 'Nieprawidłowe linie dodatkowe',
    16: 'Nieprawidłowa nazwa towaru',
    17: 'Nieprawidłowa ilość',
    18: 'Nieprawidłowa stawka PTU towaru',
    19: 'Nieprawidłowa cena towaru',
    20: 'Nieprawidłowa wartość towaru',
    21: 'Paragon nie został rozpoczęty',
    22: 'Błąd operacji storno',
    23: 'Nieprawidłowa ilość linii paragonu',
    25: 'Nieprawidłowy tekst lub nazwa kasjera',
    26: 'Nieprawidłowa wartość płatności',
    27: 'Nieprawidłowa wartość całkowita',
    28: 'Przepełnienie totalizera sprzedaży',
    30: 'Nieprawidłowa wartość płatności 2',
    32: 'Ujemny stan kasy został zastąpiony zerowym',
    34: 'Nieprawidłowa wartość lub tekst',
    35: 'Zerowe totalizery sprzedaży',
    38: 'Nieprawidłowy nazwa',
    40: 'Nie zaprogramowany nagłówek',
    51: 'Nieprawidłowa kwota',
    52: '**Niepusta tablica wycen',
    53: '**Wartość niezgodna z wyceną',
    54: '**Brak wyceny leku',
    56: '**Błąd kwoty OPŁATA',
    57: '**Przepełnienie tablicy wycen',
    58: 'Paragon offline pełny',
    82: 'Niedozwolony rozkaz',
    83: 'Zła wartość kaucji',
    84: 'Przekroczona liczba wysłanych napisów',
    99: 'Niedozwolony rozkaz',
    500: '***Zły typ paragonu',
    502: '***Nieznana ulga',
    503: '***Rabat zabroniony',
    1000: 'Błąd inicjalizacji',
    1002: 'Paragon jest już rozpoczęty',
    1003: 'Brak identyfikatora stawki PTU',
    1004: 'Nieprawidłowy rabat',
    1005: 'Nieprawidłowe dane',
    1006: 'Drukarka nie jest w trybie fiskalnym',
    1007: 'Nie zaprogramowane stawki PTU',
    1008: 'Pamięć fiskalna pełna',
    1009: 'Nieprawidłowa suma kontrolna pamięci RAM',
    1010: 'Nieprawidłowa suma kontrolna bazy danych',
    1011: 'Nieprawidłowa suma kontrolna nagłówka',
    1012: 'Nieprawidłowa suma kontrolna nazwy kasjera',
    1013: 'Nieprawidłowa suma kontrolna numeru kasy',
    1014: 'Nie powiodło się uaktualnienie danych',
    1015: 'Nie zaprogramowany numer unikatowy',
    1016: 'Brak pamięci fiskalnej',
    1017: 'Brak mechanizmu drukującego',
    1018: 'Brak wyświetlacza',
    1019: 'Pamięć fiskalna została wymieniona',
    1021: 'Urządzenie jest w trybie tylko do odczytu',
    1022: 'Nierozpoznany rozkaz',
    1023: 'Nieprawidłowy rozkaz',
    1024: 'Nieprawidłowy zakres raportu',
    1025: 'Brak danych raportu w podanym zakresie',
    1026: 'Przepełnienie bufora transmisji',
    1027: 'Niezakończony tryb fiskalny',
    1028: 'Uszkodzenie pamięci fiskalnej',
    1029: 'Przekroczony limit ograniczeń pamięci fiskalnej',
    1030: 'Uszkodzona mapa pamięci fiskalnej',
    1031: 'Rozkaz wysłany w niewłaściwym trybie',
    1032: 'Nieprawidłowy wskaźnik ramki',
    1033: '*Pamięć fiskalna jest zajęta',
    1034: 'Drukarka fiskalna jest zajęta',
    1037: 'Brak papieru',
    1046: 'Brak danych',
    1054: 'Brak dostępu',
    1070: 'Błąd graficznego nagłówka wydruku',
    1073: 'Błąd grafik wydruku',
    1075: 'Nieprawidłowa grafika',
    1076: 'Grafika już zaprogramowana',
    1078: 'Błąd transakcji SQL',
    1079: 'Pamięć na reklamy pełna',
    1083: 'Reklama w użyciu',
    1085: 'Niezgodność daty/czasu z ostatnim zapisem w PF',
    1086: 'Błąd obsługi wydruku',
    1088: 'Brak pamięci chronionej',
    1089: 'Błąd pamięci chronionej',
    1090: 'Brak miejsca w pliku wymiany',
    1091: 'Błąd bazy spisu treści',
    1092: 'Brak pozycji na paragonie',
    1093: 'Błąd stanu statusu procesów',
    1094: 'Błąd konfiguracji harmonogramów',
    1095: 'Błąd fiskalizacji',
    1096: 'Błąd połączenia z TPM',
    1097: 'Błąd serwera DNS',
    1098: 'Brak/błędny numer NIP nabywcy',
    1099: 'Błąd zapisu pamięci chronionej',
    1100: 'Blokada sprzedaży',
    1101: 'Brak danych nabywcy',
    1102: 'Błąd dostępu do pamięci chronionej',
    1103: 'Brak certyfikatów w MK',
    1104: 'Brak nazwy nabywcy',
    1105: 'Błędna suma kontrolna programu/programu PF',
    1106: 'Brak aktualizacji do pobrania',
    1107: 'Brak aktualizacji do zainstalowania',
    1108: 'Brak podłączonego zasilania',
    1109: 'Błąd numeru faktury',
    1110: 'Błąd zapisu certyfikatów',
    1111: 'Osiągnięto limit zerowań RAM',
    1112: 'Proces fiskalizacji zakończony',
    1113: 'Proces fiskalizacji niezakończony',
    1114: 'Błąd zapisu do pamięci fiskalnej',
    1115: 'Narzut zabroniony',
    1116: 'Wykonaj zaległy raport dobowy',
    1117: 'Obniżka/narzut zabroniony',
    1118: 'Osiągnięto maksymalną liczbę pozycji biletowych',
    1119: 'Wydruk z pamięci chronionej jest otwarty',
    1120: 'Wydruk z pamięci chronionej nie jest otwarty',
    9999: 'Błąd krytyczny'
 }


class NovitusError(RuntimeError):
    pass


class CommunicationError(NovitusError):
    pass


class ReplyNotImplemented(NovitusError):
    pass


class ProtocolError(NovitusError):
    def __init__(self, error_code):
        msg = error_codes.get(error_code, 'unknown error code')
        super(ProtocolError, self).__init__(
            'Protocol error occured: {} - {}'.format(error_code, msg),
            error_code,
            msg
        )
        self.error_code = error_code
        self.msg = msg

    def __repr__(self):
        return self.args[0]

    __str__ = __repr__
