# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 11:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'verbose_name_plural': 'Manufacturers'},
        ),
    ]
