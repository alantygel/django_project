# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag_analytics', '0002_loadround_insert_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadround',
            name='success',
            field=models.IntegerField(default=1),
        ),
    ]
