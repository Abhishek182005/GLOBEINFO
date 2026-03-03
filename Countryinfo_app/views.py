from django.shortcuts import render, redirect
from countryinfo import CountryInfo
import csv
import json
from django.http import HttpResponse, JsonResponse
from .country_data import GEOGRAPHICAL_FEATURES, COUNTRY_FACTS, CURRENCY_CODES, WORLD_RECORDS, COUNTRY_EXTRA_DATA


def get_all_countries():
    """Return a sorted list of all country names in Title Case."""
    try:
        all_data = CountryInfo().all()
        return sorted([name.title() for name in all_data.keys()])
    except Exception:
        return []


def _build_alpha3_lookup():
    """Build a mapping of ISO-3 code -> full country name (computed once at startup)."""
    # Manual overrides for entries missing or incomplete in the countryinfo library
    lookup = {
        'AND': 'Andorra',        'MMR': 'Myanmar',           'PRK': 'North Korea',
        'KOR': 'South Korea',    'COD': 'Dr Congo',           'COG': 'Republic Of The Congo',
        'TZA': 'Tanzania',       'CZE': 'Czech Republic',     'SSD': 'South Sudan',
        'PSE': 'Palestine',      'VAT': 'Vatican City',       'TWN': 'Taiwan',
        'IRN': 'Iran',           'SYR': 'Syria',              'VEN': 'Venezuela',
        'BOL': 'Bolivia',        'MDA': 'Moldova',            'MKD': 'North Macedonia',
        'BIH': 'Bosnia And Herzegovina', 'SOM': 'Somalia',   'YEM': 'Yemen',
        'LBY': 'Libya',          'SDN': 'Sudan',              'ERI': 'Eritrea',
        'RUS': 'Russia',         'UKR': 'Ukraine',            'KAZ': 'Kazakhstan',
        'UZB': 'Uzbekistan',     'TKM': 'Turkmenistan',       'TJK': 'Tajikistan',
        'KGZ': 'Kyrgyzstan',     'AZE': 'Azerbaijan',         'MNG': 'Mongolia',
        'LAO': 'Laos',           'KHM': 'Cambodia',           'VNM': 'Vietnam',
        'THA': 'Thailand',       'MYS': 'Malaysia',           'IDN': 'Indonesia',
        'PHL': 'Philippines',    'PNG': 'Papua New Guinea',   'NZL': 'New Zealand',
    }
    try:
        all_data = CountryInfo().all()
        for name, data in all_data.items():
            alpha3 = data.get('ISO', {}).get('alpha3', '')
            if alpha3:
                lookup.setdefault(alpha3.upper(), name.title())
    except Exception:
        pass
    return lookup

ALPHA3_TO_NAME = _build_alpha3_lookup()


def _build_name_to_alpha2():
    """Build a mapping of country name (title case) -> ISO alpha2 code."""
    manual = {
        'United States Of America': 'us', 'Russia': 'ru', 'China': 'cn',
        'India': 'in', 'United Kingdom': 'gb', 'South Korea': 'kr',
        'Pakistan': 'pk', 'Japan': 'jp', 'France': 'fr', 'Italy': 'it',
        'Germany': 'de', 'Brazil': 'br', 'Ukraine': 'ua', 'Turkey': 'tr',
        'Iran': 'ir', 'Egypt': 'eg', 'Australia': 'au', 'Israel': 'il',
        'Canada': 'ca', 'Spain': 'es', 'Netherlands': 'nl', 'Poland': 'pl',
        'Saudi Arabia': 'sa', 'Argentina': 'ar', 'Indonesia': 'id',
        'Mexico': 'mx', 'Nigeria': 'ng', 'South Africa': 'za',
        'Sweden': 'se', 'Norway': 'no', 'Switzerland': 'ch',
        'Singapore': 'sg', 'Thailand': 'th', 'Vietnam': 'vn',
        'Philippines': 'ph', 'Malaysia': 'my', 'Bangladesh': 'bd',
        'Ethiopia': 'et', 'Morocco': 'ma', 'Algeria': 'dz',
        'New Zealand': 'nz', 'Finland': 'fi', 'Chile': 'cl',
        'Colombia': 'co', 'Peru': 'pe', 'Greece': 'gr', 'Kenya': 'ke',
        'Cuba': 'cu', 'Portugal': 'pt', 'Austria': 'at', 'Belgium': 'be',
        'Denmark': 'dk', 'Iraq': 'iq', 'North Korea': 'kp',
        'Venezuela': 've', 'Romania': 'ro', 'United Arab Emirates': 'ae',
        'Czechia': 'cz', 'Hungary': 'hu',
    }
    try:
        all_data = CountryInfo().all()
        for name, data in all_data.items():
            alpha2 = data.get('ISO', {}).get('alpha2', '')
            if alpha2:
                manual.setdefault(name.title(), alpha2.lower())
    except Exception:
        pass
    return manual

NAME_TO_ALPHA2 = _build_name_to_alpha2()


def build_country_data(country_name):
    """Return a rich dictionary of data for the given country name."""
    c = CountryInfo(country_name)
    iso = {}
    flag_url = ''
    try:
        iso = c.iso()
        alpha2 = iso.get('alpha2', '').lower()
        if alpha2:
            flag_url = f"https://flagcdn.com/w320/{alpha2}.png"
    except Exception:
        pass

    borders_raw = []
    try:
        codes = c.borders() or []
        # Resolve ISO-3 codes to full country names; keep code as fallback
        borders_raw = [ALPHA3_TO_NAME.get(code.upper(), code) for code in codes]
    except Exception:
        pass

    provinces = []
    try:
        provinces = c.provinces()
    except Exception:
        pass

    wiki = ''
    try:
        wiki = c.wiki()
    except Exception:
        pass

    def safe(fn):
        try:
            return fn()
        except Exception:
            return None

    currencies_raw = safe(c.currencies) or []
    languages_raw  = safe(c.languages)  or []

    return {
        'name': country_name,
        'region': safe(c.region),
        'subregion': safe(c.subregion),
        'latlng': safe(c.latlng),
        'capital': safe(c.capital),
        'currencies': currencies_raw,          # list of code strings e.g. ['INR']
        'area': safe(c.area),
        'population': safe(c.population),
        'timezones': safe(c.timezones) or [],
        'calling_codes': safe(c.calling_codes) or [],
        'native_name': safe(c.native_name),
        'alt_spellings': safe(c.alt_spellings) or [],
        'languages': languages_raw,            # list of language code strings e.g. ['hi','en']
        'demonym': safe(c.demonym),
        'tld': safe(c.tld) or [],
        'provinces': provinces,
        'wiki': wiki,
        'iso': iso,
        'flag_url': flag_url,
        'borders': borders_raw,
        'geo_features': GEOGRAPHICAL_FEATURES.get(country_name, {}),
        'facts': COUNTRY_FACTS.get(country_name, []),
        'currencies_detail': [
            {'code': code, 'name': CURRENCY_CODES[code]['name'] if code in CURRENCY_CODES else code,
             'symbol': CURRENCY_CODES[code]['symbol'] if code in CURRENCY_CODES else ''}
            for code in currencies_raw
        ],
        'extra': COUNTRY_EXTRA_DATA.get(country_name, {}),
    }


def menu(request):
    return render(request, 'Countryinfo_app/menu.html')


def country_info(request):
    all_countries = get_all_countries()
    # Accept both POST (search form) and GET (direct link from countries list)
    country_name = None
    if request.method == 'POST':
        country_name = request.POST.get('country', '').strip().title()
    elif request.method == 'GET':
        country_name = request.GET.get('country', '').strip().title()
    if country_name:
        try:
            data = build_country_data(country_name)
            data['all_countries'] = all_countries
            return render(request, 'Countryinfo_app/country_info.html', data)
        except KeyError:
            return render(request, 'Countryinfo_app/error.html', {
                'error_message': f'Country "{country_name}" was not found. Please check the spelling and try again.',
                'retry_url': 'country_info'
            })
        except Exception as e:
            return render(request, 'Countryinfo_app/error.html', {
                'error_message': str(e),
                'retry_url': 'country_info'
            })
    return render(request, 'Countryinfo_app/country_form.html', {'all_countries': all_countries})


def country_compare(request):
    all_countries = get_all_countries()
    if request.method == 'POST':
        country1_name = request.POST.get('country1', '').strip().title()
        country2_name = request.POST.get('country2', '').strip().title()
        try:
            country1_data = build_country_data(country1_name)
            country2_data = build_country_data(country2_name)
            context = {
                'country1': country1_data,
                'country2': country2_data,
                'all_countries': all_countries,
            }
            return render(request, 'Countryinfo_app/country_compare.html', context)
        except KeyError:
            return render(request, 'Countryinfo_app/error.html', {
                'error_message': 'One or both countries were not found. Please check the spelling.',
                'retry_url': 'country_compare'
            })
        except Exception as e:
            return render(request, 'Countryinfo_app/error.html', {
                'error_message': str(e),
                'retry_url': 'country_compare'
            })
    return render(request, 'Countryinfo_app/country_compare_form.html', {'all_countries': all_countries})


def error(request):
    return render(request, 'Countryinfo_app/error.html', {
        'error_message': 'An unexpected error occurred.',
        'retry_url': 'landing_page'
    })


def country_and_capitals(request):
    try:
        countries_capitals = []
        with open("static/COUNTRIESANDCAPITAL1.csv") as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                if len(row) >= 4:
                    country_name = row[0]
                    flag_url = ''
                    try:
                        ci2 = CountryInfo(country_name)
                        iso2 = ci2.iso()
                        alpha2 = iso2.get('alpha2', '').lower()
                        if alpha2:
                            flag_url = f'https://flagcdn.com/w40/{alpha2}.png'
                    except Exception:
                        pass
                    countries_capitals.append({
                        'country': country_name,
                        'capital': row[1],
                        'currency': row[2],
                        'continent': row[3],
                        'flag_url': flag_url,
                    })
        context = {'countries_capitals': countries_capitals}
        return render(request, 'Countryinfo_app/countries_capitals.html', context)
    except FileNotFoundError:
        return render(request, 'Countryinfo_app/error.html', {
            'error_message': 'Countries data file not found.',
            'retry_url': 'landing_page'
        })
    except Exception as e:
        return render(request, 'Countryinfo_app/error.html', {
            'error_message': str(e),
            'retry_url': 'landing_page'
        })


def landing_page(request):
    all_countries = get_all_countries()
    return render(request, 'Countryinfo_app/landing_page.html', {'countries': all_countries})


def world_map(request):
    """Interactive world map — country clicked triggers AJAX fetch."""
    return render(request, 'Countryinfo_app/world_map.html')


def country_api(request, country_name):
    """JSON API endpoint used by the world map AJAX requests."""
    try:
        data = build_country_data(country_name.title())
        # currencies is a list of code strings e.g. ['INR'], languages is a list of codes e.g. ['hi','en']
        raw_currencies = data['currencies'] or []
        raw_languages  = data['languages']  or []
        currencies_out = [
            {'code': c, 'name': CURRENCY_CODES[c]['name'] if c in CURRENCY_CODES else c,
             'symbol': CURRENCY_CODES[c]['symbol'] if c in CURRENCY_CODES else ''}
            for c in raw_currencies
        ]
        payload = {
            'name': data['name'],
            'capital': data['capital'],
            'region': data['region'],
            'subregion': data['subregion'],
            'population': data['population'],
            'area': data['area'],
            'currencies': currencies_out,
            'languages': raw_languages,
            'calling_codes': data['calling_codes'],
            'tld': data['tld'],
            'flag_url': data['flag_url'],
            'wiki': data['wiki'],
            'latlng': data['latlng'],
            'timezones': data['timezones'],
            'native_name': data['native_name'],
            'iso': data['iso'],
            'borders': data.get('borders', []),
            'facts': data['facts'][:3],
            'geo_features': {
                k: v for k, v in data['geo_features'].items()
                if k in ('highest_peak', 'longest_river', 'coastline_km', 'terrain', 'climate')
            } if data['geo_features'] else {},
        }
        return JsonResponse({'status': 'ok', 'data': payload})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=404)


def currency_exchange(request):
    """Currency exchange calculator using the open.er-api.com free API (frontend fetch)."""
    return render(request, 'Countryinfo_app/currency_exchange.html', {
        'currency_codes': CURRENCY_CODES
    })


def world_records(request):
    """Global geographical and political records page."""
    # Build economy rankings from COUNTRY_EXTRA_DATA
    countries_with_data = [
        {'name': name, 'alpha2': NAME_TO_ALPHA2.get(name, ''), **data}
        for name, data in COUNTRY_EXTRA_DATA.items()
    ]

    gdp_ranking = sorted(
        [c for c in countries_with_data if c.get('gdp_billion')],
        key=lambda x: x['gdp_billion'], reverse=True
    )[:10]

    gdp_per_capita_ranking = sorted(
        [c for c in countries_with_data if c.get('gdp_per_capita')],
        key=lambda x: x['gdp_per_capita'], reverse=True
    )[:10]

    hdi_ranking = sorted(
        [c for c in countries_with_data if c.get('hdi')],
        key=lambda x: x['hdi'], reverse=True
    )[:10]

    military_ranking = sorted(
        [c for c in countries_with_data if c.get('gfp_rank')],
        key=lambda x: x['gfp_rank']
    )[:10]

    military_budget_ranking = sorted(
        [c for c in countries_with_data if c.get('military_budget')],
        key=lambda x: x['military_budget'], reverse=True
    )[:10]

    return render(request, 'Countryinfo_app/world_records.html', {
        'records': WORLD_RECORDS,
        'gdp_ranking': gdp_ranking,
        'gdp_per_capita_ranking': gdp_per_capita_ranking,
        'hdi_ranking': hdi_ranking,
        'military_ranking': military_ranking,
        'military_budget_ranking': military_budget_ranking,
    })

