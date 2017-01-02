# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-31 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_auto_20161231_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='old_price',
            new_name='discount_price',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to=b'img/category'),
        ),
    ]