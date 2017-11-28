# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError
from ..models.atencion import Atencion
from ..models.consulta import Pruebas


class ConsultaPruebasAuxiliares(models.Model):
    consulta = models.ForeignKey(Atencion)
    pruebas_auxiliares = models.ForeignKey(Pruebas, related_name='pruebas_auxiliares')
    indicacion = models.CharField(max_length=100, blank=True )
    created_time = models.TimeField(_('Hora Creada'), auto_now_add=True)
    created_at = models.DateField(_('Fecha Creada'), auto_now_add=True)

    class Meta:
        verbose_name = "Prueba Auxiliar"
        verbose_name_plural = "Pruebas Auxiliares"

    def __str__(self):
        return "%s" % self.indicacion
