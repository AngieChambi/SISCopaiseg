# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-30 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_auto_20170625_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='razon_social',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Razon social'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='representante_legal',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Representante legal'),
        ),
    ]