# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-19 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20160919_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Content for description meta tag.', max_length=255, verbose_name='Meta Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(blank=True, help_text='Comma-delimited set of SEO keywords for meta tag.', max_length=255, verbose_name='Meta Keywords'),
        ),
    ]
