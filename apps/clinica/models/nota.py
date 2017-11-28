# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError
from ..models.atenciones import Atenciones


class Notas(models.Model):
    atenciones = models.ForeignKey(Atenciones)
    descripcion = models.CharField(max_length=200, default='Mascota en buen estado',null=True, blank=True)
    created_time = models.TimeField(_('Hora Creada'), auto_now_add=True)
    created_ath = models.DateField(_('Fecha Creada'), auto_now_add=True)
    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    def __str__(self):
        return "%s" % (self.descripcion)
