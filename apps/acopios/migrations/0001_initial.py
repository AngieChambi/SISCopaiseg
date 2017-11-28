# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-26 21:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('params', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acopio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fech_acopio', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=False)),
                ('n_ticket', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Acopio',
                'verbose_name_plural': 'Acopios',
            },
        ),
        migrations.CreateModel(
            name='DetalleAcopio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kilos', models.DecimalField(decimal_places=2, max_digits=20)),
                ('precio_uni', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Precio Unitario')),
                ('total_pagar', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Precio a Pagar')),
                ('acopio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acopios.Acopio')),
            ],
            options={
                'verbose_name': 'Detalle  Acopio',
                'verbose_name_plural': 'Detalles Acopio',
            },
        ),
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8)),
                ('ubicacion', models.CharField(max_length=20)),
                ('area_cultivo', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('area_desarrollo', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('prod_estimado_tn', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('prod_estimado_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('total_parcelas', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Parcela',
                'verbose_name_plural': 'Parcelas',
            },
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_socio', models.CharField(max_length=6)),
                ('direccion', models.CharField(blank=True, max_length=50)),
                ('ciudad', models.CharField(blank=True, max_length=50)),
                ('estado', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='params.Person')),
            ],
            options={
                'verbose_name': 'Socio',
                'verbose_name_plural': 'Socios',
            },
        ),
        migrations.AddField(
            model_name='parcela',
            name='socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acopios.Socio'),
        ),
        migrations.AddField(
            model_name='detalleacopio',
            name='parcela',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acopios.Parcela'),
        ),
        migrations.AddField(
            model_name='acopio',
            name='socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acopios.Socio'),
        ),
    ]
