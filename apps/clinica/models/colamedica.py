# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError


from ..models.mascota import Mascota
from apps.sad.models import User


class ColaMedica(models.Model):
    fuente_atencion = models.CharField(max_length=100)
    mascota = models.ForeignKey(Mascota, blank=True, null=False)
    medico = models.ForeignKey(User, blank=True, null=False)
    fecha = models.DateField(capfirst(_('Fecha Creada')), auto_now_add=True, )
    hora = models.TimeField(capfirst(_('Hora Registrada')), auto_now_add=True, )
    descripcion = models.CharField(max_length=100)
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    is_actived = models.BooleanField(_('Actived'), default=False)

    class Meta:
        verbose_name = "Cola Medica"
        verbose_name_plural = "Colas Medicas"
        permissions = (
            ('colamedica', 'Can ALL colamedica'),
        )

    def __str__(self):
        return "%s" % (self.mascota)
