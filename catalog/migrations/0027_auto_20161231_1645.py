# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-31 16:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_auto_20161231_1612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount_price',
            new_name='old_price',
        ),
    ]