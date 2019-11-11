import os
import logging
import requests
import time
from operator import itemgetter

api_key = os.environ.get("NEWS_API_KEY_2")
categories = ['business', 'entertainment', 'health', 'science', 'sports', 'technology', None]
country_codes = {
    'ar': {'name':'Argentina',      'language': 'es'},
    'au': {'name':'Australia',      'language': 'en'},
    'at': {'name':'Austria',        'language': 'de'},
    'be': {'name':'Belgium',        'language': 'nl'},  # 'nl' most likely followed by 'fr', some 'de'
    'br': {'name':'Brazil',         'language': 'pt'},
    'bg': {'name':'Bulgaria',       'language': 'bg'},
    'ca': {'name':'Canada',         'language': 'en'},
    'cn': {'name':'China',          'language': 'zh'},
    'zh': {'name':'China',          'language': 'zh'},
    'co': {'name':'Columbia',       'language': 'es'},
    'cu': {'name':'Cuba',           'language': 'es'},
    'cz': {'name':'Czech Republic', 'language': 'cs'},
    'eg': {'name':'Egypt',          'language': 'ar'},
    'es': {'name':'Spain',          'language': 'es'},
    'fr': {'name':'France',         'language': 'fr'},
    'de': {'name':'Germany',        'language': 'de'},
    'gr': {'name':'Greece',         'language': 'el'},
    'hk': {'name':'Hong Kong',      'language': 'zh'},  # 'zh', some 'en'
    'hu': {'name':'Hungary',        'language': 'hu'},
    'in': {'name':'India',          'language': 'hi'},  # 'hi', 'en' ?
    'id': {'name':'Indonesia',      'language': 'id'},
    'ie': {'name':'Ireland',        'language': 'en'},
    'il': {'name':'Israel',         'language': 'he'},
    'is': {'name':'Israel',         'language': 'he'},  # 'he' + 'en'
    'it': {'name':'Italy',          'language': 'it'},
    'jp': {'name':'Japan',          'language': 'ja'},
    'lv': {'name':'Latvia',         'language': 'lv'},
    'lt': {'name':'Lithuania',      'language': 'lt'},
    'my': {'name':'Malaysia',       'language': 'ms'},  # 'ms' ? 'malay'
    'mx': {'name':'Mexico',         'language': 'es'},
    'ma': {'name':'Morocco',        'language': 'fr'},  # 'fr'most biz/gov/media, ar used more by population
    'nl': {'name':'Netherlands',    'language': 'nl'},
    'nz': {'name':'New Zealand',    'language': 'en'},
    'ng': {'name':'Nigeria',        'language': 'en'},
    'no': {'name':'Norway',         'language': 'no'},
    'pk': {'name':'Pakistan',       'language': 'ud'},
    'ph': {'name':'Philippines',    'language': 'en'},  # 'en' (none for filipino)
    'pl': {'name':'Poland',         'language': 'pl'},
    'pt': {'name':'Portugal',       'language': 'pt'},
    'ro': {'name':'Romania',        'language': 'ro'},
    'ru': {'name':'Russia',         'language': 'ru'},
    'sa': {'name':'Saudi Arabia',   'language': 'ar'},
    'rs': {'name':'Serbia',         'language': 'sr'},
    'sg': {'name':'Singapore',      'language': 'en'},  # 'en' (malay, ms, is official but en is used for biz/gov/edu)
    'sk': {'name':'Slovakia',       'language': 'sk'},
    'si': {'name':'Slovenia',       'language': 'sl'},
    'za': {'name':'South Africa',   'language': 'en'},
    'kr': {'name':'South Korea',    'language': 'ko'},
    'se': {'name':'Sweden',         'language': 'se'},  # 'se'=api  'sv'=iso
    'ch': {'name':'Switzerland',    'language': 'de'},  # 'de' @74%, other official: fr @ 21, it @ 4, and romansh @ 1)
    'tw': {'name':'Taiwan',         'language': 'zh'},
    'th': {'name':'Thailand',       'language': 'th'},
    'tr': {'name':'Turkey',         'language': 'tr'},
    'ae': {'name':'UAE',            'language': 'en'},
    'ua': {'name':'Ukraine',        'language': 'uk'},
    'gb': {'name':'United Kingdom', 'language': 'en'},
    'us': {'name':'United States',  'language': 'en'},
    've': {'name':'Venezuela',      'language': 'es'}
}
logger = logging.getLogger(__name__)
meta_source_list = []


def generate_sources(sources):
    for source in sources:
        yield source


def request_sources_for_country(alpha2_code, src_cat=None):
    if src_cat is None:
        endpoint = f'https://newsapi.org/v2/top-headlines?country={alpha2_code}&apiKey={api_key}'
    else:
        endpoint = f'https://newsapi.org/v2/top-headlines?country={alpha2_code}&category={src_cat}&apiKey={api_key}'
    response = requests.get(endpoint)
    if response.json()['status'] == 'ok':
        data = response.json()['articles']
        data_gen = (source for source in data)
        return generate_sources(data_gen)
    elif response.json()['status'] == 'error':
        logger.log(level=logging.ERROR, msg=f'Error Code: {response.json()["code"]} Message: {response.json()["message"]}')
        return None


def request_top_sources():
    response = requests.get("https://newsapi.org/v2/sources?apiKey=9cc20bcd3bf94baea37a0f95ecf28b8a")
    if response.json()['status'] == 'ok':
        data = response.json()['sources']
        top_sources_gen = (source for source in data)
        return top_sources_gen
    elif response.json()['status'] == 'error':
        logger.log(level=logging.ERROR, msg=f'Code: {response.json()["code"]}, Message: {response.json()["message"]}')
        return None


def build_top_sources(generated_top_sources):
    for source in generated_top_sources:
        new_source = {
            'id'         : source['id'],
            'name'       : source['name'],
            'country'    : source['country'],
            'language'   : source['language'],
            'category'   :[source['category']],
            'url'        : source['url'],
            'description': source['description'] }
        try:
            meta_source_list.index(new_source)  # check to see if this source is present in list, do nothing if it is
        except ValueError:  # thrown if source is not found in list, catch and add new source
            meta_source_list.append(new_source)


def build_national_sources(generated_sources, alpha2_code, src_cat):
    for source in generated_sources:
        new_src = {
            'id'         : source['source']['id'],
            'name'       : source['source']['name'],
            'country'    : alpha2_code,
            'language'   : country_codes.get(alpha2_code).get('language'),
            'category'   : [ src_cat ],
            'url'        : None,
            'description': None }
        try:
            idx = list(map(itemgetter('name'), meta_source_list)).index(new_src['name']) # get idx of source with new_src.name, raises ValueError if not found
            if new_src['category'][0] not in meta_source_list[idx]['category']: # append new_src.category to matched source.category if not present
                meta_source_list[idx]['category'].append(new_src['category'][0])
        except ValueError:
            meta_source_list.append(new_src)


def write_sources(src_list):
    with open('meta_sources.txt', 'a+') as outfile:
        for idx in range(0, len(meta_source_list)):
            if idx == 0:
                outfile.write('{\n' + str(meta_source_list[idx]) + ',')
            elif idx == len(meta_source_list) - 1:
                outfile.write('\n' + str(meta_source_list[idx]) + '\n}')
            else:
                outfile.write('\n' + str(meta_source_list[idx]) + ',')
            logger.log(level=logging.INFO, msg=f'Success: {str(meta_source_list[idx])}')
            print(f'New Source: {str(meta_source_list[idx])}')
        return True


def run():
    print('requesting top_data')
    top_data = request_top_sources()
    if top_data:
        print('have top_data -- building')
        build_top_sources(top_data)
    time.sleep(240)  # Roughly 410 api calls required to capture targeted source data,
                     # these keep the entire process within the max of 500 calls/day and 250 calls/12-hours;
                     # but it takes a day to run =( ....at least no worrying about multi-threading    *<1[8,^)-|-<=;
    for code in country_codes:
        for category in categories:
            print(f'requesting data from {code} of category type {category}')
            country_data = request_sources_for_country(alpha2_code=code, src_cat=category)
            if country_data:
                print(f'have {category} data from {code}')
                build_national_sources(country_data, code, category)
            time.sleep(240)
    print('preparing to write sources')
    successful = write_sources(meta_source_list)
    logger.log(level=logging.INFO, msg=f'Sources to File = {successful}')
    print('operation complete')



if __name__ == '__main__':
    print('starting mock')
    run()





