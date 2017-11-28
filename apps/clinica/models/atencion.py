# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError
#Impors  Models
from ..models.colamedica import ColaMedica
from ..models.atenciones import Atenciones
from ..models.mascota import Mascota
from ..models.consulta import Diagnostico, Tratamiento, Pruebas, HallasgosClinicos

# Create your models here.
class Atencion(models.Model):
    atenciones = models.ForeignKey(Atenciones)
#Consulta
    motivo_atencion = models.CharField(max_length=300)
    temperatura = models.CharField(max_length=50)
    fc = models.CharField(max_length=50)
    fr = models.CharField(max_length=50)
    kg = models.CharField(max_length=50)
    porcentaje = models.CharField(max_length=50)
    tlc = models.CharField(max_length=50)
    anamnesis = models.CharField(max_length=200)
    hallasgos_clinicos = models.ManyToManyField(HallasgosClinicos, max_length=300)
    #diagnostico = models.ManyToManyField(Diagnostico, max_length=300)
    dx = models.CharField(max_length=300)
    pronostico = models.CharField(max_length=300)
    #pruebas_auxiliares = models.ManyToManyField(Pruebas, max_length=300)
    #tratamiento = models.ManyToManyField(Tratamiento, max_length=300)
    observacion = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Atencion"
        verbose_name_plural = "Atenciones"
        permissions = (
            ('atencion', 'Can ALL atencion'),
        )
    def __str__(self):
        return "%s" % (self.motivo_atencion)
