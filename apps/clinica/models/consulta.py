# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError

from apps.clinica.models.mascota import Mascota
# Create your models here.

class Diagnostico(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return "%s" % (self.nombre)
class HallasgosClinicos(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return "%s" % (self.nombre)
class Pruebas(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return "%s" % (self.nombre)
class Tratamiento(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return "%s" % (self.nombre)
