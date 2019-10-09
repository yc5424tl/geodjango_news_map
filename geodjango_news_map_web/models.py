import os
from django.conf import settings
from django.db import models


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(SETTINGS_DIR))
CHORO_MAP_ROOT = os.path.join(PROJECT_ROOT, 'geodjango_news_map_web/media/query_html_result/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'geodjango_news_map_web/static'),]

class QueryManager(models.Manager):
    def create_query(self, argument, date_created, query_type, author=None, choropleth=None, choro_html=None, data=None, date_range_end=None, date_range_start=None,public=False):
        news_query = self.create(
            _argument =argument,
            _author=author,
            _choropleth=choropleth,
            _choro_html=choro_html,
            _data=data,
            _date_created=date_created,
            _date_range_end=date_range_end,
            _date_range_start=date_range_start,
            _filename=self.filename,
            _public=public,
            _query_type=query_type)
        return news_query


class QueryResultSet(models.Model):
    query_types = ( ('headlines', 'Headlines'), ('all', 'All') )
    _argument = models.CharField(max_length=500)
    _choropleth = models.TextField(max_length=2000000, blank=True)
    _choro_html = models.TextField(max_length=200000, blank=True)
    _data = models.CharField(max_length=200000, blank=True)
    _date_created = models.DateField(auto_now_add=True)
    _date_last_modified = models.DateField(default=None, null=True, blank=True)
    _date_range_end = models.DateField(default=None, null=True, blank=True)
    _date_range_start = models.DateField(default=None, null=True, blank=True)
    _filename = models.TextField(max_length=700, blank=True)
    _filepath = models.TextField(max_length=1000, blank=True)
    _public = models.BooleanField(default=False)
    _query_type = models.CharField(default='all', choices=query_types, max_length=50)
    _author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='queries')
    _archived = models.BooleanField(default=False)

    @property
    def choropleth(self) -> str:
        return self._choropleth

    @choropleth.setter
    def choropleth(self, new_choro: str) -> None:
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
    def filepath(self):
        return self._filepath

    @property
    def author(self):
        return self._author

    @property
    def public(self):
        return self._public

    @property
    def query_type(self):
        return self._query_type

    @property
    def date_created(self):
        return self._date_created

    @property
    def date_range_end(self):
        return self._date_range_end

    @property
    def date_range_start(self):
        return self._date_range_start

    @property
    def date_last_modified(self):
        return self._date_last_modified

    @date_last_modified.setter
    def date_last_modified(self, new_date):
        self._date_last_modified = new_date

    def __str__(self):
        details = 'Argument = ' + self._argument + '\n' + '' \
                  'Query Type = ' + str(self._date_created) + '\n' + \
                  'Author = ' + str(self._author) + '\n' + \
                  'Archived = ' + str(self._archived) + '\n' + \
                  'Public = ' + str(self._public) + '\n' + \
                  'Data[:500] = ' + self._data[:500] + '\n' + \
                  'Choropleth HTML[:500] = ' + self._choro_html[:500]
        if self._filename:
            details = details + '\n' + 'Filename = ' + self._filename
        return details

    @property
    def argument(self):
        return self._argument

    @argument.setter
    def argument(self, new_argument):
        if isinstance(new_argument, str):
            self._argument = new_argument
        else:
            raise Exception("Invalid Value for argument")

    @property
    def date_created_readable(self):
        return '%s/%s/%s' % (self._date_created.month, self._date_created.day, self._date_created.year)

    @property
    def archived(self):
        return self._archived

    @archived.setter
    def archived(self, is_archived):
        if isinstance(is_archived, bool):
            self._archived = is_archived
        else:
            raise TypeError('Property "archived" must be type bool.')


class Source(models.Model):
    source_categories = (('business', 'Business'),
        ('entertainment', 'Entertainment'),
        ('general', 'General'),
        ('health', 'Health'),
        ('science', 'Science'),
        ('sports', 'Sports'),
        ('technology', 'Technology'))
    _api_id = models.CharField(max_length=300)
    _category = models.CharField(max_length=300, choices=source_categories)
    _country = models.CharField(max_length=200)
    _country_alpha_code = models.CharField(max_length=3)
    _description = models.CharField(max_length=2000)
    _language = models.CharField(max_length=500)
    _name = models.CharField(max_length=500)
    _url = models.URLField(max_length=1000)

    def __str__(self):
        return '%s - %s(%s)' % (self._name, self._country, self._country_alpha_code)

    @property
    def country(self):
        return self._country

    @property
    def name(self):
        return self._name

    @property
    def language(self):
        return self._language

    @property
    def category(self):
        return self._category

    @property
    def url(self):
        return self._url


class Article(models.Model):
    _article_url = models.URLField(max_length=1000)
    _author = models.CharField(max_length=150)
    _date_published = models.DateTimeField()
    _description = models.CharField(max_length=2500)
    _image_url = models.URLField(max_length=1000, default=None, blank=True, null=True)
    _query = models.ForeignKey(QueryResultSet, on_delete=models.CASCADE, related_name='articles')
    _source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='articles')
    _title = models.CharField(max_length=300)

    def __str__(self):
        return '%s - %s, %s %s' % \
               (self._title, self._author, self.date_published, self._source.name)

    @property
    def source(self):
        return self._source

    @property
    def source_country(self):
        return self.source.country

    @property
    def article_url(self):
        return self._article_url

    @property
    def author(self):
        return self._author

    @property
    def date_published(self):
        return self._date_published

    @property
    def description(self):
        return self._description

    @property
    def image_url(self):
        return self._image_url

    @property
    def query(self):
        return self._query

    @property
    def title(self):
        return self._title


class Post(models.Model):
    _title = models.CharField(max_length=300, default='', null=True, blank=True)
    _body = models.CharField(max_length=50000, default='', null=True, blank=True)
    _date_published = models.DateTimeField(auto_now_add=True)
    _author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='posts')
    _date_last_edit = models.DateTimeField(auto_now_add=True)
    _query = models.OneToOneField(QueryResultSet, on_delete=models.PROTECT)
    _public = models.BooleanField(default=False)

    @property
    def author(self):
        return self._author

    @property
    def title(self):
        return self._title

    @property
    def body(self):
        return self._body

    @property
    def date_published(self):
        return self._date_published

    @property
    def date_last_edit(self):
        return self._date_last_edit

    @property
    def public(self):
        return self._public

    @property
    def query(self):
        return self._query


    def get_choro_map(self):
        if self._query:
            qrs_pk = self._query.pk
            qrs = QueryResultSet.objects.get(pk=qrs_pk)
            if qrs.choropleth:
                return qrs.choropleth
            else:
                return None



class Comment(models.Model):
    _post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='comments')
    _body = models.CharField(max_length=25000)
    _date_published = models.DateTimeField(auto_now_add=True)
    _date_last_edit = models.DateTimeField(auto_now_add=True)
    _author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comments')

    def __str__(self):
        return "comment from " + self.author.first_name + ' ' +  self.author.last_name + ' on the post ' + "'" + self.post.title + "', made " + str(self.date_published)

    @property
    def post(self):
        return self._post

    @post.setter
    def post(self, new_post):
        self._post = new_post

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, new_body):
        self._body = new_body

    @property
    def date_published(self):
        return self._date_published

    @date_published.setter
    def date_published(self, new_date):
        self._date_published = new_date

    @property
    def date_last_edit(self):
        return self._date_last_edit

    @date_last_edit.setter
    def date_last_edit(self, new_date):
        self._date_last_edit = new_date

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        self._author = new_author


#======================================================================================#

# enum help from
#   https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63