# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20170629_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='batch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='products.Batch'),
        ),
    ]
