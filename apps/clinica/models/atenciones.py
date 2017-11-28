# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError
from ..models.colamedica import ColaMedica

from config.settings.base import MEDIA_ROOT
class Atenciones(models.Model):
    colamedica = models.ForeignKey(ColaMedica, unique=True, blank=True)
    estado = models.BooleanField(default=False)
    created_ath = models.DateTimeField(_('Fecha Creada'), auto_now_add=True)

    class Meta:
        verbose_name = "Atencione"
        verbose_name_plural = "Atencioness"
        permissions = (
            ('atenciones', 'Can ALL atenciones'),
        )
    def __str__(self):
        return "%s" % (self.colamedica)


class ArchivosAdjuntos(models.Model):
    atenciones = models.ForeignKey(Atenciones)
    file = models.FileField( upload_to='archivos' )  # Modelo para subir un imaenes y archivos (Pruebas)
    created_time = models.TimeField(_('Hora Creada'), auto_now_add=True)
    created_ath = models.DateField(_('Fecha Creada'), auto_now_add=True)
    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"

    def __str__(self):
        return "%s" % (self.atenciones)
