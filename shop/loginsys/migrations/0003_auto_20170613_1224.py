# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginsys', '0002_auto_20170613_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favourites',
            field=models.ManyToManyField(blank=True, related_name='amateurs', to='products.Product'),
        ),
    ]
