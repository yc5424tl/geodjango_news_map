import json
import logging
from logging import Logger

import pycountry
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.views.decorators.csrf import csrf_exempt

from .constructor import Constructor
from .forms import CustomUserCreationForm, NewQueryForm, NewPostForm, EditPostForm, EditCommentForm, NewCommentForm
from .geo_data_mgr import GeoDataManager
from .geo_map_mgr import GeoMapManager
from .models import QueryResultSet, Source, Post, Comment, Category
from .query_mgr import Query

logger = Logger(__name__)

constructor = Constructor()
geo_data_mgr = GeoDataManager()
geo_map_mgr = GeoMapManager()


@transaction.atomic
def index(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'general/index.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('view_user', user.pk)
        else:
            messages.info(request, message=form.errors)
            form = CustomUserCreationForm()
            return render(request, 'general/new_user.html', {'form': form})
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'general/new_user.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('view_user', user.pk)
        form = AuthenticationForm()
        messages.error(request, 'Incorrect Password and/or Username', extra_tags='error')
        return render(request, 'general/login_user.html', {'form': form})

    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'general/login_user.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'Logout Successful', extra_tags='alert')


@login_required()
def new_query(request):
    if request.method == 'GET':
        form = NewQueryForm()
        return render(request, 'general/new_query.html', {'search_form': form})

    elif request.method == 'POST':
        geo_data_mgr.verify_geo_data()
        constructor.get_sources()

        query_mgr = Query(arg=request.POST.get('_argument'), focus=request.POST.get('_query_type'))
        query_mgr.get_endpoint()
        article_data = query_mgr.execute_query()
        query_set = QueryResultSet.objects.create(_query_type=query_mgr.focus, _argument=query_mgr.arg, _data=article_data, _author=request.user)
        query_set.save()

        article_list = constructor.build_article_data(article_data, query_set)
        for article in article_list:
            code = geo_map_mgr.map_source(source_country=article.source_country)
            geo_data_mgr.add_result(code)

        data_tup = geo_map_mgr.build_choropleth(query_mgr.arg, query_mgr.focus, geo_data_mgr)
        if data_tup is None:
            return redirect('index', messages='build choropleth returned None')
        else:
            global_map = data_tup[0]
            filename = data_tup[1]
            qrs = QueryResultSet.objects.get(pk=query_set.pk)
            qrs._choro_html = global_map.get_root().render()
            qrs._filename = filename
            qrs._author = User.objects.get(pk=request.user.pk)
            qrs._choropleth = global_map._repr_html_()
            qrs.save()

        return redirect('view_query', query_set.pk)


@login_required()
def view_query(request, query_result_set_pk):
    qrs = get_object_or_404(QueryResultSet, pk=query_result_set_pk)
    return render(request, 'general/view_query.html', {
        'query': qrs,
        'query_author': qrs.author,
        'articles': qrs.articles.all(),
        'choro_map': qrs.choropleth,
        'choro_html': qrs.choro_html,
        'filename': qrs.filename
    })


@login_required()
def view_public_posts(request):
    posts = Post.objects.order_by('-id').all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'general/view_public_posts.html', {'posts': posts})



@login_required()
def delete_comment(request, comment_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        post_pk = comment.post.pk
        if comment.author.pk == request.user.pk:
            comment.delete()
            messages.info(request, 'Comment Deleted')
        return redirect('view_post', post_pk)



@login_required()
def delete_query(request, query_pk):
    QueryResultSet.objects.filter(pk=query_pk).delete()
    messages.info(request, "Query Successfully Deleted")
    return redirect('new_query')


@login_required()
def view_user(request, member_pk):
    try:
        member = User.objects.get(pk=member_pk)
        try:
            last_post = member.posts.order_by('-id')[0]
        except IndexError:
            last_post = None
        try:
            recent_posts = member.posts.order_by('-id')[1:5]
        except IndexError:
            recent_posts = None
        try:
            recent_comments = None
            has_comments = member.comments.all()[0]
            if has_comments:
                recent_comments = member.comments.all()[0:5]
        except IndexError:
            recent_comments = None
        try:
            recent_queries = None
            has_queries = member.queries.all()[0]
            if has_queries:
                recent_queries = member.queries.all()[1:5]
        except IndexError:
            recent_queries = None

        return render(request, 'general/view_user.html', {
            'member': member,
            'posts': recent_posts,
            'comments': recent_comments,
            'last_post': last_post,
            'queries': recent_queries
        })
    except User.DoesNotExist:
        raise Http404


@login_required()
def new_post(request):
    if request.method == 'GET':
        form = NewPostForm()
        qrs_pk = form['query_pk'].value()
        qrs = get_object_or_404(QueryResultSet, pk=qrs_pk)
        return render(request, 'general/new_post.html', {
            'form': form,
            'query': qrs
        })
    elif request.method == 'POST':
        form = NewPostForm(request.POST)
        if request.user.is_authenticated:
            try:
                pk = request.user.pk
                author = User.objects.get(pk=pk)
                if form.is_valid():
                    title = form.cleaned_data['_title']
                    public = request.POST.get('save_radio')
                    body = form.cleaned_data['_body']
                    qrs_pk = request.POST.get('query_pk')
                    qrs = QueryResultSet.objects.get(pk=qrs_pk)
                    post = Post(_title=title, _public=public, _body=body, _query=qrs, _author=author)
                    post.save()
                    qrs.archived = True
                    qrs.save()
                    return redirect('view_post', post.pk)
                else:
                    print('Errors = ' + form.errors) # TODO apply useful logic
            except User.DoesNotExist:
                raise Http404
    else:
        raise Http404


@login_required()
def update_post(request, post_pk):
    return render(request, 'general/update_post.html')


@login_required()
def update_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        form = EditCommentForm(instance=comment)
        return render(request, 'general/update_comment.html', {'form': form, 'comment': comment})
    elif request.method == 'POST':
        form = EditCommentForm()
        if form.is_valid():
            form.save()
            messages.info(request, 'Comment Updated!')
        else:
            messages.error(request, form.errors)
        return redirect('view_comment', comment_pk=comment_pk)


@login_required()
def view_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, 'Post Details Updated')
        else:
            messages.error(request, form.errors)
        return redirect('post_details', post_pk=post_pk)
    else:
        post = Post.objects.get(pk=post_pk)
        qrs = post.query
        articles = post.query.articles.all()
        if post.author.id == request.user.id:
            edit_post_form = EditPostForm(instance=Post) #Pre-populate form with the post's current field values
            return render(request, 'general/view_post.html', {'post': post, 'edit_post_form': edit_post_form, 'query': qrs, 'articles': articles})
        else:
            return render(request, 'general/view_post.html', {'post': post, 'query': qrs, 'articles': articles})


def view_sources(request):

    constructor.get_sources()

    source_dict_list = [{
        'country':     source.country,
        'name':        source.name,
        'language':    source.language,
        'categories': [category.name for category in source.categories],
        'url':         source.url}
    for source in Source.objects.all()]

    category_dict_list = [{
        category.name: [{
           'country': source.country,
           'name': source.name,
           'language': source.language,
           'url': source.url
        } for source in category.source_set]
    } for category in Category.objects.all()]

    return render(request, 'general/view_sources.html', {'sources': source_dict_list, 'categories': category_dict_list})


def lang_a2_to_name(source):
    try:
        name = pycountry.languages.lookup(source.language).name
        return name
    except LookupError:
        return source.language


def country_a2_to_name(source):
    try:
        name = pycountry.countries.lookup(source.country).name
        return name
    except LookupError:
        return source.country


@login_required()
def delete_post(request):
    pk = request.POST['post_pk']
    post = get_object_or_404(Post, pk=pk)
    if post.author.id == request.user.id:
        post.delete()
        messages.info(request, 'Post Removed')
        return redirect('index')
    else:
        messages.error(request, 'Action Not Authorized')


@login_required()
def new_comment(request, post_pk):
    if request.method == 'GET':
        form = NewCommentForm()
        post = Post.objects.get(pk=post_pk)
        return render(request, 'general/new_comment.html', {'post': post, 'form': form})
    elif request.method == 'POST':
        c_post = Post.objects.get(pk=post_pk)
        c_body = request.POST.get('_body')
        c_author = User.objects.get(pk=request.user.pk)
        c = Comment.objects.create(_post=c_post, _body=c_body, _author=c_author)
        c.save()
        return redirect('view_comment', c.pk)


@login_required()
def view_comment(request, comment_pk):
    try:
        comment = Comment.objects.get(pk=comment_pk)
        return render(request, 'general/view_comment.html', {'comment': comment})
    except Comment.DoesNotExist:
        raise Http404


@login_required()
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    last_url = request.POST['redirect_url']
    messages.info(request, 'Failed to Delete Comment')
    return redirect(request, last_url)

@csrf_exempt
@permission_required('geodjango_news_map.add_source', 'geodjango_news_map.change_source')
def import_sources(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            payload_dict = json.loads(request.POST.get('data'))
            logger.log(level=logging.INFO, msg=f'JSON DATA FROM POST ->\n\n {payload_dict}')

            try:
                updated_count = 0
                new_count = 0
                source_data = payload_dict['sources']
                for source in source_data:

                    try: # Check db for Source
                        record = Source.objects.get(_name=source['name'])

                        for cat in source['categories']: # Source exists in DB
                            try: # Verify categories in DB
                                category = Category.objects.get(name=cat)
                            except ValueError: # Not in DB, create and add.
                                category = Category(name=cat)
                                category.save()
                            if category not in record.categories: # Category exists but not yet for Source
                                record.categories.append(category)
                        updated_count += 1

                    except Source.DoesNotExist:
                        new_source = Source.objects.create(
                                            _name=source['name'],
                                            _country=source['country'],
                                            _language=source['language'],
                                            _url=source['url'] if source['url'] else None)
                        for cat in source['categories']:
                            try:
                                category = Category.objects.get(name=cat)
                                new_source.categories.add(category)
                            except ValueError:
                                new_source.categories_set.create(name=cat)
                        new_source.save()
                        new_count += 1
                logger.log(level=logging.INFO, msg=f'Finished importing source data. \nUpdated: {updated_count}\nNew: {new_count}')
                return HttpResponse(status=201)

            except ValueError:
                logger.log(level=logging.INFO, msg=f'POST request to import sources failed to have sources as a data key.')

        elif request.user.is_authenticated is False:
            return HttpResponse(status=401)


#TODO def password_reset(request)


def view_choro(request, query_pk):
    qrs = QueryResultSet.objects.get(pk=query_pk)
    return render(request, 'general/view_choro.html', {
        'query': qrs
    })


@login_required()
def view_test_page(request):
    return render(request, 'general/test_choro.html')


@login_required()
def get_sources_by_country(request):
    new_sources = constructor.build_sources_by_country()