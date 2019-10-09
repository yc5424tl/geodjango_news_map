# Generated by Django 2.2.5 on 2019-10-09 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_api_id', models.CharField(max_length=300)),
                ('_category', models.CharField(choices=[('business', 'Business'), ('entertainment', 'Entertainment'), ('general', 'General'), ('health', 'Health'), ('science', 'Science'), ('sports', 'Sports'), ('technology', 'Technology')], max_length=300)),
                ('_country', models.CharField(max_length=200)),
                ('_country_alpha_code', models.CharField(max_length=3)),
                ('_description', models.CharField(max_length=2000)),
                ('_language', models.CharField(max_length=500)),
                ('_name', models.CharField(max_length=500)),
                ('_url', models.URLField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='QueryResultSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_argument', models.CharField(max_length=500)),
                ('_choropleth', models.TextField(blank=True, max_length=2000000)),
                ('_choro_html', models.TextField(blank=True, max_length=200000)),
                ('_data', models.CharField(blank=True, max_length=200000)),
                ('_date_created', models.DateField(auto_now_add=True)),
                ('_date_last_modified', models.DateField(blank=True, default=None, null=True)),
                ('_date_range_end', models.DateField(blank=True, default=None, null=True)),
                ('_date_range_start', models.DateField(blank=True, default=None, null=True)),
                ('_filename', models.TextField(blank=True, max_length=700)),
                ('_filepath', models.TextField(blank=True, max_length=1000)),
                ('_public', models.BooleanField(default=False)),
                ('_query_type', models.CharField(choices=[('headlines', 'Headlines'), ('all', 'All')], default='all', max_length=50)),
                ('_archived', models.BooleanField(default=False)),
                ('_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='queries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_title', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('_body', models.CharField(blank=True, default='', max_length=50000, null=True)),
                ('_date_published', models.DateTimeField(auto_now_add=True)),
                ('_date_last_edit', models.DateTimeField(auto_now_add=True)),
                ('_public', models.BooleanField(default=False)),
                ('_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('_query', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='geodjango_news_map_web.QueryResultSet')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_body', models.CharField(max_length=25000)),
                ('_date_published', models.DateTimeField(auto_now_add=True)),
                ('_date_last_edit', models.DateTimeField(auto_now_add=True)),
                ('_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('_post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='geodjango_news_map_web.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_article_url', models.URLField(max_length=1000)),
                ('_author', models.CharField(max_length=150)),
                ('_date_published', models.DateTimeField()),
                ('_description', models.CharField(max_length=2500)),
                ('_image_url', models.URLField(blank=True, default=None, max_length=1000, null=True)),
                ('_title', models.CharField(max_length=300)),
                ('_query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='geodjango_news_map_web.QueryResultSet')),
                ('_source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles', to='geodjango_news_map_web.Source')),
            ],
        ),
    ]
