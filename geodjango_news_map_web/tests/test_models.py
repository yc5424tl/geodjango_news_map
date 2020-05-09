from django.test import TestCase
from geodjango_news_map.geodjango_news_map_web.models import QueryResultSet
import datetime
from django.contrib.auth.models import User

# class QueryManagerTest(TestCase):
#
#     def setUp(self):
#         self.user_1 = User.objects.create_user('test_user_1', 'test_1@localhost.com', 'user_1_pw')
#
#     @classmethod
#     def setUpTestData(cls):
#         QueryManager.objects.create(
#             arg='test_arg',
#             date_created=datetime.datetime.now(),
#             query_type='ALL',
#             author=User.objects.get(username='test_user_1'),
#             choropleth=None,
#             choro_html=None,
#             data=None,
#             date_range_end=None,
#             date_range_start=None,
#             public=False,
#         )




 # TODO date_created to datetime -> auto_add_now -> django.utils.timezone.now()
class QueryResultSetTest(TestCase):


    def setUp(self):

        self.user_1 = User.objects.create_user('test_user_1', 'test_1@localhost.com', 'user_1_pw')

        self.qrs = QueryResultSet.objects.create(
            _argument='test_argument',
            _choropleth='',
            _choro_html='',
            _data='',
            _date_created=datetime.date.today(),
            _date_last_modified=None,
            _date_range_end=None,
            _date_range_start=None,
            _filename='',
            _filepath='',
            _public=False,
            _query_type='all',
            _author=User.objects.get(username='test_user_1'),
            _archived=False,
            _article_count=0,
            _article_data_len=0
        )


    def test_argument_label(self):
        qrs = self.qrs
        field_label = qrs._meta.get_field('_argument').verbose_name
        self.assertEquals(field_label, 'argument')

