# Generated by Django 2.2.7 on 2019-11-16 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodjango_news_map_web', '0002_auto_20191111_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='_categories',
            field=models.ManyToManyField(related_name='sources', to='geodjango_news_map_web.Category'),
        ),
    ]
