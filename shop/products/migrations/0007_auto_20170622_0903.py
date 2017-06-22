# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import products.models
import products.storage


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20170620_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='date',
        ),
        migrations.AddField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sku',
            name='image',
            field=models.ImageField(storage=products.storage.OverwriteStorage(), upload_to=products.models.get_upload_path),
        ),
    ]