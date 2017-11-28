# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-29 14:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0004_auto_20170522_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultaDiagnostico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_diagnostico', models.CharField(choices=[('Afirmativo', 'Afirmativo'), ('Presuntivo', 'Presuntivo')], max_length=50)),
                ('descripcion', models.CharField(blank=True, default='Mascota en buen estado', max_length=200, null=True)),
                ('created_time', models.TimeField(auto_now_add=True, verbose_name='Hora Creada')),
                ('created_ath', models.DateField(auto_now_add=True, verbose_name='Fecha Creada')),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.Atencion')),
                ('diagnostico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosticos', to='clinica.Atencion')),
            ],
            options={
                'verbose_name_plural': 'Consultas Diagnosticos',
                'verbose_name': 'Consulta Diagnostico',
            },
        ),
    ]
