# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError

from smart_selects.db_fields import ChainedForeignKey

from apps.sad.models import User
# Create your models here.


class prueba(models.Model):
    nombre= models.CharField(max_length=255)
    class Meta:
        verbose_name = "prueba"
        verbose_name = "pruebas"
    def __str__(self):
        return  self.nombre

class Especie(models.Model):
    nombre = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"
    def __str__(self):
        return "%s" % self.nombre


class Raza(models.Model):
    especie = models.ForeignKey(Especie, related_name="config_especie")
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"

    def __str__(self):
        return "%s" % self.nombre

class Color(models.Model):
    especie = models.ForeignKey(Especie, related_name='config_color_especie')
    raza = ChainedForeignKey(
		Raza,
		chained_field="especie",
		chained_model_field="especie",
		show_all=False,
		auto_choose=True,
        sort=True
	)

    nombre = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"

    def __str__(self):
        return "%s" % self.nombre
