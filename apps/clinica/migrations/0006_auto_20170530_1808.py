# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-30 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0005_consultadiagnostico'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultaPruebasAuxiliares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicacion', models.CharField(blank=True, max_length=100)),
                ('created_time', models.TimeField(auto_now_add=True, verbose_name='Hora Creada')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Fecha Creada')),
            ],
            options={
                'verbose_name': 'Prueba Auxiliar',
                'verbose_name_plural': 'Pruebas Auxiliares',
            },
        ),
        migrations.CreateModel(
            name='ConsultaTratamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicacion', models.CharField(blank=True, max_length=100)),
                ('created_time', models.TimeField(auto_now_add=True, verbose_name='Hora Creada')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Fecha Creada')),
            ],
            options={
                'verbose_name': 'Tratamiento',
                'verbose_name_plural': 'Tratamientos',
            },
        ),
        migrations.RemoveField(
            model_name='atencion',
            name='diagnostico',
        ),
        migrations.RemoveField(
            model_name='atencion',
            name='pruebas_auxiliares',
        ),
        migrations.RemoveField(
            model_name='atencion',
            name='tratamiento',
        ),
        migrations.AlterField(
            model_name='consultadiagnostico',
            name='diagnostico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosticos', to='clinica.Diagnostico'),
        ),
        migrations.AddField(
            model_name='consultatratamiento',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.Atencion'),
        ),
        migrations.AddField(
            model_name='consultatratamiento',
            name='tratamientos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tratamientos', to='clinica.Tratamiento'),
        ),
        migrations.AddField(
            model_name='consultapruebasauxiliares',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.Atencion'),
        ),
        migrations.AddField(
            model_name='consultapruebasauxiliares',
            name='pruebas_auxiliares',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pruebas_auxiliares', to='clinica.Pruebas'),
        ),
    ]
