# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_batch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='sku',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='batch', to='products.SKU'),
        ),
    ]