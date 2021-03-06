from datetime import datetime
from typing import NoReturn
import pycountry
from django.conf import settings
from django.db import models


class QueryManager(models.Manager):
    def create_query(self,
                     arg             :str,
                     date_created    :datetime,
                     query_type      :str,
                     author          :str=None,
                     choropleth      :str=None,
                     choro_html      :str=None,
                     data            :str=None,
                     date_range_end  :datetime.date=None,
                     date_range_start:datetime.date=None,
                     public          :bool=False):
                return self.create(
                                _argument         =arg,
                                _author           =author,
                                _choropleth       =choropleth,
                                _choro_html       =choro_html,
                                _data             =data,
                                _date_created     =date_created,
                                _date_range_end   =date_range_end,
                                _date_range_start =date_range_start,
                                _filename         =self.filename,
                                _public           =public,
                                _query_type       =query_type)



class QueryResultSet(models.Model):
    query_types         = ( ('headlines', 'Headlines'), ('all', 'All') )
    _argument           = models.CharField(max_length=500)
    _choropleth         = models.TextField(max_length=2000000, blank=True)
    _choro_html         = models.TextField(max_length=200000, blank=True)
    _data               = models.CharField(max_length=200000, blank=True)
    _date_created       = models.DateField(auto_now_add=True)
    _date_last_modified = models.DateField(default=None, null=True, blank=True)
    _date_range_end     = models.DateField(default=None, null=True, blank=True)
    _date_range_start   = models.DateField(default=None, null=True, blank=True)
    _filename           = models.TextField(max_length=700, blank=True)
    _filepath           = models.TextField(max_length=1000, blank=True)
    _public             = models.BooleanField(default=False)
    _query_type         = models.CharField(default='all', choices=query_types, max_length=50)
    _author             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='queries')
    _archived           = models.BooleanField(default=False)
    _article_count      = models.IntegerField(default=0)
    _article_data_len   = models.IntegerField(default=0)


    @property
    def article_count(self) -> int:
        return self._article_count

    @property
    def article_data_len(self) -> int:
        return self._article_data_len

    @property
    def choropleth(self) -> str:
        return self._choropleth

    @choropleth.setter
    def choropleth(self, new_choro: str) -> NoReturn:
        self._choropleth = new_choro

    @property
    def choro_html(self) -> str:
        return self._choro_html

    @property
    def data(self) -> str:
        return self._data

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def author(self) -> settings.AUTH_USER_MODEL:
        return self._author

    @property
    def public(self) -> bool:
        return self._public

    @property
    def query_type(self) -> str:
        return self._query_type

    @property
    def date_created(self) -> datetime.date:
        return self._date_created

    @property
    def date_range_end(self) -> datetime.date:
        return self._date_range_end

    @property
    def date_range_start(self) -> datetime.date:
        return self._date_range_start

    @property
    def date_last_modified(self) -> datetime.date:
        return self._date_last_modified

    @date_last_modified.setter
    def date_last_modified(self, new_date) -> NoReturn:
        self._date_last_modified = new_date

    def __str__(self):
        details = f'Argument: {self._argument}\n Query Type: {self._query_type}\n Author: {self._author}\n Archived: {self._archived}\n' \
                  f'Public: {self._public}\n Data[:500]: {self._data[:500]}\n ChoroHTML: {self._choro_html[:500]}'
        if self._filename:
            details = f'{details}\nFilename = {self._filename}'
        return details

    @property
    def argument(self) -> str:
        return self._argument

    @argument.setter
    def argument(self, new_argument) -> NoReturn:
        if isinstance(new_argument, str):
            self._argument = new_argument
        else:
            raise Exception("Invalid Value for argument")

    @property
    def date_created_readable(self) -> str:
        return f'{self._date_created.month}, {self._date_created.day}, {self._date_created.year}'

    @property
    def archived(self) -> bool:
        return self._archived

    @archived.setter
    def archived(self, is_archived: bool) -> NoReturn:
        if isinstance(is_archived, bool):
            self._archived = is_archived
        else:
            raise TypeError('Property "archived" must be type bool.')


class Category(models.Model):
    _name = models.CharField(max_length=50)

    @property
    def name(self) -> str:
        return self._name


class Source(models.Model):
    _name       = models.CharField(max_length=500)
    _country    = models.CharField(max_length=3)
    _language   = models.CharField(max_length=100)
    # _categories = models.ManyToManyField(Category, related_name='sources', through='Section')
    _categories = models.ManyToManyField(Category, related_name='sources')
    _url        = models.URLField(blank=True, default='', max_length=150)
    _verified   = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f'{self._name}, {self._country}, {self._country}'

    @property
    def verified(self) -> bool:
        return self._verified

    @verified.setter
    def verified(self, is_verified) -> NoReturn:
        self._verified = is_verified

    @property
    def country(self) -> str:
        return self._country

    @property
    def country_full_name(self) -> str:
        try:
            return pycountry.countries.lookup(self.country).name
        except LookupError:
            return self._country

    @property
    def name(self) -> str:
        return self._name

    @property
    def language(self) -> str:
        return self._language

    @property
    def language_full_name(self) -> str:
        try:
            return pycountry.languages.lookup(self.language).name
        except LookupError:
            return self._language

    @property
    def categories(self):
        return self._categories

    @property
    def url(self) -> str:
        return self._url


class Article(models.Model):
    _article_url    = models.URLField(max_length=1000)
    _author         = models.CharField(max_length=150)
    _date_published = models.DateTimeField()
    _description    = models.CharField(max_length=2500)
    _image_url      = models.URLField(max_length=1000, default=None, blank=True, null=True)
    _query          = models.ForeignKey(QueryResultSet, on_delete=models.CASCADE, related_name='articles')
    _source         = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='articles')
    _title          = models.CharField(max_length=300)

    def __str__(self):
        return f'{self._title}, {self._author}, {self._date_published}, {self._source.name}'

    @property
    def source(self) -> Source:
        return self._source

    @property
    def source_country(self) -> str:
        return self._source.country

    @property
    def article_url(self) -> str:
        return self._article_url

    @property
    def author(self) -> str:
        return self._author

    @property
    def date_published(self) -> datetime.date:
        return self._date_published

    @property
    def description(self) -> str:
        return self._description

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def query(self) -> QueryResultSet:
        return self._query

    @property
    def title(self) -> str:
        return self._title


class Post(models.Model):
    _title          = models.CharField(max_length=300, default='', null=True, blank=True)
    _body           = models.CharField(max_length=50000, default='', null=True, blank=True)
    _date_published = models.DateTimeField(auto_now_add=True)
    _author         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='posts')
    _date_last_edit = models.DateTimeField(auto_now_add=True)
    _query          = models.OneToOneField(QueryResultSet, on_delete=models.PROTECT)
    _public         = models.BooleanField(default=False)

    @property
    def author(self) -> settings.AUTH_USER_MODEL:
        return self._author

    @property
    def title(self) -> str:
        return self._title

    @property
    def body(self) -> str:
        return self._body

    @property
    def date_published(self) -> datetime.date:
        return self._date_published

    @property
    def date_last_edit(self) -> datetime.date:
        return self._date_last_edit

    @property
    def public(self) -> bool:
        return self._public

    @property
    def query(self) -> QueryResultSet:
        return self._query

    def get_choro_map(self) -> str or NoReturn:
        if self._query:
            qrs_pk = self._query.pk
            qrs = QueryResultSet.objects.get(pk=qrs_pk)
            return qrs.choropleth if qrs.choropleth else None


class Comment(models.Model):
    _post           = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='comments')
    _body           = models.CharField(max_length=25000)
    _date_published = models.DateTimeField(auto_now_add=True)
    _date_last_edit = models.DateTimeField(auto_now_add=True)
    _author         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comments')

    def __str__(self) -> str:
        return f'Comment from {self._author.first_name} {self._author.last_name} on {self.date_published} to post "{self.post.title}", made {self.date_published}'

    @property
    def post(self) -> Post:
        return self._post

    @post.setter
    def post(self, new_post) -> NoReturn:
        self._post = new_post

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, new_body) -> NoReturn:
        self._body = new_body

    @property
    def date_published(self) -> datetime.date:
        return self._date_published

    @date_published.setter
    def date_published(self, new_date) -> NoReturn:
        self._date_published = new_date

    @property
    def date_last_edit(self) -> datetime.date:
        return self._date_last_edit

    @date_last_edit.setter
    def date_last_edit(self, new_date) -> NoReturn:
        self._date_last_edit = new_date

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, new_author) -> NoReturn:
        self._author = new_author

#======================================================================================#
# enum help from
#   https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63