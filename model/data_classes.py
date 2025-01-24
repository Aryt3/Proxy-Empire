from enum import Enum
import json

# https://gist.githubusercontent.com/Aryt3/a9662a94a6f4dc833de84d580c0db077/raw/7d28585f22c9dec0fdd8654bf5d4bf7a570f4553/country_codes_2024.jsonc
countries_data = json.load(open('./data/countries.jsonc', 'r'))

# Extract all country iso codes from JSON
country_codes = [countries_data[region][country]['iso-3166-2'].lower() for region in countries_data for country in countries_data[region]]

CountryEnum = Enum('CountryEnum', [(code.upper(), code) for code in list(set(country_codes))] + [("NONE", None)])


class ProtocolEnum(Enum):
    HTTP = 'http'
    HTTPS = 'https'
    SOCKS4 = 'socks4'
    SOCKS5 = 'socks5' 
    NONE = None