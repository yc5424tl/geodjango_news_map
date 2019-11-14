import logging
import os
from datetime import datetime

from dateutil.parser import parse

from .models import Article, QueryResultSet, Source

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


