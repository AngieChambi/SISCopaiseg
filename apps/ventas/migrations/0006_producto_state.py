# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-29 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_auto_20170625_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]
