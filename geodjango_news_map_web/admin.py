from django.contrib import admin

from .models import Source, Post, QueryResultSet, Article, Comment, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('_title','_author', '_date_published', '_source', '_query')

@admin.register(QueryResultSet)
class QueryResultSetAdmin(admin.ModelAdmin):
    list_display = ('_argument', '_query_type', '_filename', '_filepath', '_author', '_archived', '_date_created', '_public', '_choropleth')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('_title', '_date_published', '_author', '_query', '_public', '_date_last_edit')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('_body', '_date_published', '_date_last_edit', '_author', '_post')

#
# class SourceInstanceInline(admin.TabularInline):
#     model = Source

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ( '_name', '_country', '_language', '_url')
    list_editable = ('_country', '_language', '_url')
    list_filter = ('_country', '_language')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['_name']