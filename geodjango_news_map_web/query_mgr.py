import logging
import os
import requests
import builtins
from datetime import datetime
from newsapi import NewsApiClient


logger = logging.getLogger(__name__)
api_key = os.environ.get('NEWS_API_KEY_2')
news_api = NewsApiClient(api_key=api_key)


class Query:
    def __init__(self, argument, focus, from_date=None, to_date=None, endpoint=None):
        self.argument = argument
        self.focus = focus
        self.from_date = from_date
        self.to_date = to_date
        self.endpoint = endpoint


    def filename(self):
        date_created = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f'api_data-{self.argument}_{self.focus}-{date_created}.json'
        return filename


    def validate_date_range(self):
        has_range =  self.to_date - self.from_date > 0
        is_past = datetime.now() - self.to_date > 0
        return has_range and is_past


    def get_endpoint(self):
        valid_date_range = self.validate_date_range() if self.from_date and self.to_date else False
        if valid_date_range:
            if self.focus == 'all':
                pass
            elif self.focus == 'headlines':
                pass
            else:
                return False
        elif not valid_date_range:
            if self.focus == 'all':
                self.endpoint = f'https://newsapi.org/v2/everything?q={self.argument}&apiKey={api_key}'
            elif self.focus == 'headlines':
                self.endpoint = f'https://newsapi.org/v2/top-headlines?c'
            else:
                return False
        else:
            return False
        return True



    def execute_query(self):
        response = requests.get(self.endpoint)
        print(f'\nRESPONSE\nresponse == {response.json()}\nEND RESPONSE\n\n')
        article_count = response.json()['totalResults']
        article_data = response.json()['articles']

        if article_count > 100:
            pages = ((article_count//100) -1)
            if pages > 100:
                pages = 5
            for p in range(2, pages):
                print(f'Requesting Page # {p}')
                try:
                    page = requests.get(f'{self.endpoint}&page={p}')
                    print(f'Before adding to article_data, len = {len(article_data)}')
                    article_data += page.json()['articles']
                    print(f'Before adding to article_data, len = {len(article_data)}')

                except requests.exceptions.RequestException as rE:
                    print(f'RequestException while getting article_data @ page # {p}')
                    logger.exception(rE)
                    continue
                except builtins.KeyError as kE:
                    print(f'KeyErrorException while getting article_data on {p}')
                    logger.exception(kE)
                    continue

        return article_data


    def to_file(self, data):
        try:
            with open(self.filename(), 'w+') as file:
                file.write(str(data))
        except UnicodeEncodeError:
            logger.exception(UnicodeEncodeError, 'UnicodeEncodeError during writing articles.json to file (QueryManager)')
        except AttributeError:
            logger.exception(AttributeError, 'AttributeException during writing articles.json to file (QueryManager)')
        except TypeError:
            logger.exception(TypeError, 'TypeError while ')
