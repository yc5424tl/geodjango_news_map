from datetime import datetime
from . models import Article, Post, QueryResultSet, Source
from logging import Logger
from dateutil.parser import parse
import json
import os
import requests


logger = Logger(__name__)


class Constructor:

    def new_article(self, response_data, query_set: QueryResultSet):
        source = self.verify_source(response_data['source']['name'])
        date_published = self.verify_date(response_data['publishedAt'])
        article_url = response_data['url']
        image_url = response_data['urlToImage'] if response_data['urlToImage'] is not None else None
        try:
            description = self.verify_str(response_data['description']) if response_data['description'] is not None else 'Unavailable'
        except UnicodeDecodeError:
            description = 'Unavailable'
        try:
            title = self.verify_str(response_data['title'])
        except UnicodeDecodeError:
            title = 'Unavailable'
        try:
            author = self.verify_str(response_data['author'])
            if author is None:
                author = 'Unknown'
        except UnicodeEncodeError:
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
                logger.exception(f'{e} propagating from constructor.verify_source({source_name})')
                return False
        elif not source_name:
            logger.error(f'{source_name} retrieval failed.')
            return False



    def get_sources(self):
        try:
            db_has_sources = Source.objects.get(pk=1)
            print('past db_has_sources')
            return bool(db_has_sources)
        except (UnicodeDecodeError, FileNotFoundError, Source.DoesNotExist, TypeError):
            try:
                with open('./geodjango_news_map_web/static/js/sources.json') as sources:
                    source_list = json.load(sources)
                    print('loaded sources to source_list in constructor')
                    print(f'type(source_list) = {type(source_list)}')
                    print(f'source_list.keys = {source_list.keys()}')
                    print(f'source_list[sources] type = {type(source_list["sources"])}')
                    print(f'source_list[sources] = {source_list["sources"]}')
                    for source_data in source_list['sources']:
                        try:
                            print(f"id = {source_data['id']}")
                            print(f"name = {source_data['name']}")
                            print(f"description = {source_data['description']}")
                            print(f"url = {source_data['url']}")
                            print(f"category = {source_data['category']}")
                            print(f"language = {source_data['language']}")
                            print(f"country = {source_data['country']}")
                            new_source = Source(_api_id=source_data['id'],
                                                _name = source_data['name'],
                                                _description=source_data['description'],
                                                _url = source_data['url'],
                                                _category = source_data['category'],
                                                _language = source_data['language'],
                                                _country = source_data['country'])
                            new_source.save()
                        except TypeError:
                            logger.error(f'{TypeError} while constructing new Source')
            except (FileNotFoundError, UnicodeDecodeError):
                print('final attempt, calling self.build_sources()')
                source_dict = self.build_sources
                print(f'sources = {source_dict}')
                self.record_sources(source_dict)
                return True


    def filter_source(self, source_data):
        try:
            new_source = self.new_source(source_data)
            if new_source:
                new_source.save()
        except TypeError:
            print(f'TypeError while building_sources with {source_data}')
            logger.error(f'{TypeError} while building new Source')


    def build_sources(self):
        response = requests.get(os.getenv('NEWS_API_SOURCES_URL'))
        response_data = response.json()
        source_list = list(filter(self.filter_source, response_data))
        return (source for source in source_list)

    @staticmethod
    def record_sources(source_json):
        try:
            with open('sources.json', 'a') as json_file:
                json_file.write(str(source_json))
        except UnicodeEncodeError:
            logger.exception(UnicodeEncodeError, 'UnicodeDecodeError in QueryManager.build_sources()')
        except AttributeError:
            logger.exception(AttributeError, 'AttributeError in QueryManager.build_sources()')
        except KeyError:
            logger.exception(KeyError, 'KeyError in QueryManager.build_sources()')



    def new_source(self, data):
        try:
            name = self.verify_str(data['name'])
        except UnicodeDecodeError:
            name = self.verify_str(data['id'])
        try:
            description = self.verify_str(data['description'])
        except UnicodeDecodeError:
            description = 'Unavailable'
        if name:
            return Source(_api_id=data['id'],
                          _category=data['category'],
                          _country=data['country'],
                          _description=description,
                          _language=data['language'],
                          _name=name,
                          _url=data['url'])
        else:
            return False