from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Source, Post, QueryResultSet, Article, Comment, Category


@admin.register(Article)
class ArticleAdmin(OSMGeoAdmin):
    list_display = ('_author', '_date_published', '_source', '_title', '_query')

@admin.register(QueryResultSet)
class QueryResultSetAdmin(OSMGeoAdmin):
    list_display = ('_argument', '_query_type', '_filename', '_filepath', '_author', '_archived', '_date_created', '_public', '_choropleth')

@admin.register(Post)
class PostAdmin(OSMGeoAdmin):
    list_display = ('_title', '_date_published', '_author', '_query', '_public', '_date_last_edit')

@admin.register(Comment)
class CommentAdmin(OSMGeoAdmin):
    list_display = ('_body', '_date_published', '_date_last_edit', '_author', '_post')

@admin.register(Source)
class SourceAdmin(OSMGeoAdmin):
    list_display = ('_country', '_language', '_name', '_url')
    modifiable = ('_country', '_url', '_language')

@admin.register(Category)
class CategoryAdmin(OSMGeoAdmin):
    list_display = ('_name',)