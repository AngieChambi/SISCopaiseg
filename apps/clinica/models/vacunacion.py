# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError

from apps.ventas.models.Producto import Producto
from ..models.atenciones import Atenciones

TIPO_VACUNACION=(
    ('cita', "cita"),
    ('consulta', "consulta")
)

class Vacunacion(models.Model):
    atenciones = models.ForeignKey(Atenciones, blank=True)
    motivo = models.CharField(max_length= 150, blank=True)
    created_ath = models.DateTimeField(_(u'Fecha Creada'), auto_now_add=True)
    tipo_vacunacion = models.CharField(_(u'Tipo Vacunación'), max_length=50, choices = TIPO_VACUNACION, blank=True)
    vacuna = models.ForeignKey(Producto, max_length=100,  blank=True)
    dosis = models.CharField(max_length=50, blank=True)
    observacion = models.TextField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "vacunacion"
        verbose_name_plural = "vacunaciones"
        permissions = (
            ('vacunaciones', 'Can ALL vacunaciones'),
        )
    def __str__(self):
        return "%s" % (self.motivo)
