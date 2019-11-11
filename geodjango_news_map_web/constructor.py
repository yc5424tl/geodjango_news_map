import builtins
import json
import os
from datetime import datetime
from logging import INFO, ERROR
import logging
import requests
from dateutil.parser import parse

from .models import Article, QueryResultSet, Source, Category

api_key = os.environ.get('NEWS_API_KEY_2')

logger = logging.getLogger(__name__)

class Constructor:

    def new_article(self, response_data, query_set: QueryResultSet):
        source = self.verify_source(response_data['source']['name'])
        date_published = self.verify_date(response_data['publishedAt'])
        article_url = response_data['url']
        image_url = response_data['urlToImage'] if response_data['urlToImage'] is not None else None
        try:
            description = self.verify_str(response_data['description']) if response_data['description'] is not None else 'Unavailable'
        except UnicodeDecodeError as e:
            logger.log(level=logging.DEBUG, msg=f'UnicodeDecodeError while parsing description for new article: {e}\nSource Data: {response_data}')
            description = 'Unavailable'
        try:
            title = self.verify_str(response_data['title'])
        except UnicodeDecodeError as e:
            logger.log(level=logging.DEBUG, msg=f'UnicodeDecodeError while parsing title for new article: {e}\nSource Data {e}')
            title = 'Unavailable'
        try:
            author = self.verify_str(response_data['author'])
            if author is None:
                author = 'Unknown'
        except UnicodeEncodeError as e:
            logger.log(level=logging.DEBUG, msg=f'UnicodeDecodeError while parsing author for new article: {e}\nSource Data {e}')
            author = 'Unknown'
        if source:
            new_article = Article(
                _article_url=article_url,
                _author=author,
                _date_published=date_published,
                _description=description,
                _image_url=image_url,
                _query=query_set,
                _source=source,
                _title=title)
            new_article.save()
            return new_article
        else:
            return False


    def build_article_data(self, article_data_list, query_set: QueryResultSet):
        article_list = []
        for article_data in article_data_list:
            new_article = self.new_article(article_data, query_set)
            if new_article:
                article_list.append(new_article)
        return article_list

    @staticmethod
    def verify_str(data):
        if data and isinstance(data, str):
            return data
        else:
            return None

    def verify_date(self, data):
        f_data = self.format_date(data)
        if data and isinstance(f_data, datetime):
            return f_data
        else:
            return None

    @staticmethod
    def format_date(data):
        try:
            return parse(data)
        except ValueError:
            return None


    @staticmethod
    def verify_source(source_name):
        if source_name:
            try:
                source = Source.objects.get(_name=source_name)
                return source
            except (AttributeError, Source.DoesNotExist) as e:
                logger.log(level=logging.ERROR, msg=f'{e} propagating from constructor.verify_source({source_name})')
                return False
        elif not source_name:
            logger.error(f'{source_name} retrieval failed.')
            return False



    def get_sources(self):
        try:
            db_has_sources = Source.objects.get(pk=1)
            logger.log(level=INFO, msg='past db_has_sources')
            return bool(db_has_sources)
        except (UnicodeDecodeError, FileNotFoundError, Source.DoesNotExist, TypeError):
            try:
                with open('./geodjango_news_map_web/static/js/sources.json') as sources:
                    source_list = json.load(sources)
                    logger.log(level=INFO, msg='loaded sources to source_list in constructor')
                    logger.log(level=INFO, msg=f'type(source_list) = {type(source_list)}')
                    logger.log(level=INFO, msg=f'source_list.keys = {source_list.keys()}')
                    logger.log(level=INFO, msg=f'source_list[sources] type = {type(source_list["sources"])}')
                    logger.log(level=INFO, msg=f'source_list[sources] = {source_list["sources"]}')
                    for source_data in source_list['sources']:
                        try:
                            logger.log(level=INFO, msg=f"id = {source_data['id']}")
                            logger.log(level=INFO, msg=f"name = {source_data['name']}")
                            logger.log(level=INFO, msg=f"description = {source_data['description']}")
                            logger.log(level=INFO, msg=f"url = {source_data['url']}")
                            logger.log(level=INFO, msg=f"category = {source_data['category']}")
                            logger.log(level=INFO, msg="language = {source_data['language']}")
                            logger.log(level=INFO, msg="country = {source_data['country']}")
                            # new_source = Source(_api_id=source_data['id'],
                            #                     _name = source_data['name'],
                            #                     _description=source_data['description'],
                            #                     _url = source_data['url'],
                            #                     _category = source_data['category'],
                            #                     _language = source_data['language'],
                            #                     _country = source_data['country'])
                            new_source = Source(_name = source_data['name'],
                                                _language = source_data['language'],
                                                _country = source_data['country'],
                                                _categories = [source_data['category']])
                            new_source.save()
                        except TypeError:
                            logger.error(f'{TypeError} while constructing new Source')
            except (FileNotFoundError, UnicodeDecodeError):
                # logger.log(level=INFO, msg='final attempt, calling self.build_sources()')
                # top_source_dict = self.build_top_sources
                # logger.log(level=INFO, msg=f'sources = {top_source_dict}')
                # country_source_dict = self.build_sources_by_country
                # meta_dict = dict(country_source_dict, **top_source_dict)
                # self.record_sources(top_source_dict)
                # self.record_sources(country_source_dict)
                return True


    def filter_source(self, source_data):
        try:
            new_source = self.new_source(source_data)
            if new_source:
                new_source.save()
        except TypeError:
            logger.log(level=INFO, msg=f'TypeError while building_sources with {source_data}')
            logger.error(f'{TypeError} while building new Source')


    # def build_top_sources(self):
    #     response = requests.get(os.getenv('NEWS_API_SOURCES_URL'))
    #     response_data = response.json()
    #     source_list = list(filter(self.filter_source, response_data))
    #     return (source for source in source_list)


    # def build_sources_by_country(self):
    #     country_codes = {'ar': 'Argentina',      # 'es'
    #                      'au': 'Australia',      # 'en'
    #                      'at': 'Austria',        # 'de'
    #                      'be': 'Belgium',        # 'nl' most likely followed by 'fr', some 'de'
    #                      'br': 'Brazil',         # 'pt'
    #                      'bg': 'Bulgaria',       # 'bg'
    #                      'ca': 'Canada',         # 'en'
    #                      'cn': 'China',          # 'zh'
    #                      'zh': 'China',          # 'zh'
    #                      'co': 'Columbia',       # 'es'
    #                      'cu': 'Cuba',           # 'es'
    #                      'cz': 'Czech Republic', # 'cs'
    #                      'eg': 'Egypt',          # 'ar'
    #                      'es': 'Spain',          # 'es'
    #                      'fr': 'France',         # 'fr'
    #                      'de': 'Germany',        # 'de'
    #                      'gr': 'Greece',         # 'el'
    #                      'hk': 'Hong Kong',      # 'zh', some 'en'
    #                      'hu': 'Hungary',        # 'hu'
    #                      'in': 'India',          # 'hi', 'en' ?
    #                      'id': 'Indonesia',      # 'id'
    #                      'ie': 'Ireland',        # 'en'
    #                      #'il': 'Israel',        # 'he'
    #                      'is': 'Israel',         # 'he' + 'en'
    #                      'it': 'Italy',          # 'it'
    #                      'jp': 'Japan',          # 'ja'
    #                      'lv': 'Latvia',         # 'lv'
    #                      'lt': 'Lithuania',      # 'lt'
    #                      'my': 'Malaysia',       # 'ms' ? 'malay'
    #                      'mx': 'Mexico',         # 'es'
    #                      'ma': 'Morocco',        # 'fr'  -- most biz/gov/media/mid-lrg companies use, although ar is used more by the population
    #                      'nl': 'Netherlands',    # 'nl'
    #                      'nz': 'New Zealand',    # 'en'
    #                      'ng': 'Nigeria',        # 'en'
    #                      'no': 'Norway',         # 'no'
    #                      'pk': 'Pakistan',       # 'ud'
    #                      'ph': 'Philippines',    # 'en' (none for filipino)
    #                      'pl': 'Poland',         # 'pl'
    #                      'pt': 'Portugal',       # 'pt'
    #                      'ro': 'Romania',        # 'ro'
    #                      'ru': 'Russia',         # 'ru'
    #                      'sa': 'Saudi Arabia',   # 'ar'
    #                      'rs': 'Serbia',         # 'sr' > Serbian
    #                      'sg': 'Singapore',      # 'en' (malay, ms, is official but en is used for biz/gov/edu)
    #                      'sk': 'Slovakia',       # 'sk' ? slovak
    #                      'si': 'Slovenia',       # 'sl' ? slovenian
    #                      'za': 'South Africa',   # 'en'
    #                      'kr': 'South Korea',    # 'ko'
    #                      'se': 'Sweden',         # 'se'=api  'sv'=iso
    #                      'ch': 'Switzerland',    # 'de' (@74%, other officials are fr @ 21, it @ 4, and romansh @ 1)
    #                      'tw': 'Taiwan',         # 'zh'
    #                      'th': 'Thailand',       # 'th' ? thai=iso
    #                      'tr': 'Turkey',         # 'tr' ?=iso
    #                      'ae': 'UAE',            # 'en'
    #                      'ua': 'Ukraine',        # 'uk' ?=iso
    #                      'gb': 'United Kingdom', # 'en'
    #                      'us': 'United States',  # 'en'
    #                      've': 'Venezuela'}      # 'es'}


    # def get_sources_for_country(self, alpha2_code: str, category=None):
    #     endpoint = None
    #     if not category:
    #         endpoint = f'https://newsapi.org/v2/top-headlines?country={alpha2_code}&apiKey={api_key}'
    #     elif category:
    #         endpoint = f'https://newsapi.org/v2/top-headlines?country={alpha2_code}&category={category}&apiKey={api_key}'
    #     response = requests.get(endpoint)
    #     logger.log(level=INFO, msg=f'response=={response.json()}')
    #     count = response.json()['totalResults']
    #     data = response.json()['articles']
    #
    #     if count > 100:
    #         pages = ((count // 100) - 1)
    #         logger.log(level=INFO, msg=f'Raw page count for {endpoint} is {pages} from {count} articles.')
    #         if pages > 100:
    #             pages = 10
    #         for p in range(2, pages):
    #             logger.log(level=INFO, msg=f'Requesting page #{p}')
    #             try:
    #                 page = requests.get(f'{endpoint}&page={p}')
    #                 logger.log(level=INFO, msg=f'Before adding to article_data, len = {len(data)}')
    #                 data += page.json()['articles']
    #                 logger.log(level=INFO, msg=f'Before adding to article_data, len = {len(data)}')
    #
    #             except (requests.exceptions.RequestException, builtins.KeyError) as e:
    #                 logger.log(level=INFO, msg=f'RequestException while getting article_data @ page # {p}')
    #                 logger.log(level=ERROR, msg=logger.exception(e))
    #                 continue
    #             except builtins.KeyError as kE:
    #                 logger.log(level=INFO, msg=f'KeyErrorException while getting article_data on {p}')
    #                 logger.log(level=ERROR, msg=logger.exception(kE))
    #                 continue
    #         source_list = list(filter(self.filter_source, data))
    #         return (source for source in source_list)
    #
    #
    # @staticmethod
    # def record_sources(source_json):
    #     try:
    #         with open('sources.json', 'a') as json_file:
    #             json_file.write(str(source_json))
    #     except UnicodeEncodeError:
    #         logger.exception(UnicodeEncodeError, 'UnicodeDecodeError in QueryManager.build_sources()')
    #     except AttributeError:
    #         logger.exception(AttributeError, 'AttributeError in QueryManager.build_sources()')
    #     except KeyError:
    #         logger.exception(KeyError, 'KeyError in QueryManager.build_sources()')



    def new_source(self, data: dict):

        categories = []

        if 'categories' in data.keys():
            for cat in data['categories']:
                try:
                    category = Category.objects.get(_name=cat)
                except ValueError:
                    category = Category(_name=cat)
                    category.save()
                categories.append(category)

        if 'category' in data.keys():
            try:
                cat = Category.objects.get(_name=data['category'])
            except ValueError:
                cat = Category(_name=data['category'])
            cat.save()
            categories.append(cat)

        try:
            name = self.verify_str(data['name'])
        except UnicodeDecodeError:
            name = self.verify_str(data['id']) if 'id' in data.keys() else None

        url = data['url'] if 'url' in data.keys() else None

        if name:
            return Source(_categories  = categories,
                          _country     = data['country'],
                          _language    = data['language'],
                          _name        = name,
                          _url         = url)
        else:
            logger.log(level=logging.DEBUG, msg=f'Name/ID unavailable from Source data:\n{data}')
            return False