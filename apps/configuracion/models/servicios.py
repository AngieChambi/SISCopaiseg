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


class Servicios(models.Model):
    nombre= models.CharField(max_length=255)
    precio = models.CharField(max_length=50)
    descripcion = models.TextField(u'descripción', max_length=300)
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    is_actived = models.BooleanField(_('Actived'), default=False)
    class Meta:
        verbose_name = "Servicio"
        verbose_name = "Servicios"
    def __str__(self):
        return  "%s" % self.nombre
