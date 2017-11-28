# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError

from apps.sad.models import User
from apps.clinica.models.mascota import Mascota

CARACTER = (
    ('tranquilo', "Tranquilo"),
    ('agresivo', "Agresivo"),
    ('nervioso', "Nervioso")
)

ACTIVIDAD = (
    ('alta', "Alta"),
    ('normal', "Normal"),
    ('baja', "Baja")
)

HABITAT = (
    ('casa', "Casa"),
    ('azotea', "Azotea"),
    ('campo', "Campo"),
    ('patio', "Patio"),
    ('criadero', "Criadero"),
    ('jardin', "Jardin"),
    ('calle', "Calle")
)

ALIMENTACION = (
    ('balanceada', "Balanceada seca"),
    ('lata', "Lata"),
    ('casera', "Casera"),
    ('huevos', "Huevos"),
    ('huevos', "Otros")
)

APTITUP = (
    ('compañia', "Compañia"),
    ('guardia', "Guardia"),
    ('trabajo', "Trabajo"),
    ('deporte', "Deporte"),
    ('casa', "Casa")
)

CONVIVE = (
    ('Si', "Sí"),
    ('No', "No")
)

# Create your models here.

class Historial(models.Model):
    num_historia = models.CharField(max_length=40, unique=True)
    veterinario = models.ForeignKey(User)
    mascota = models.ForeignKey(Mascota, verbose_name=_('Mascota'), null=True, blank=True,)
    created_ath = models.DateTimeField(_('Fecha Creada'), auto_now_add=True)
#reseña de la amscota
    caracter = models.CharField(max_length=100, choices=CARACTER ,null=True, blank=True)
    actividad = models.CharField(max_length=100, choices=ACTIVIDAD ,null=True, blank=True)
    habitar = models.CharField(max_length=100, choices=HABITAT ,null=True, blank=True)
    alimentacion = models.CharField(max_length=100, choices=ALIMENTACION , null=True, blank=True)
    aptitup = models.CharField(max_length=100, choices=APTITUP ,null=True, blank=True)
    convive = models.CharField(max_length=100, choices=CONVIVE ,null=True, blank=True)

    class Meta:
        verbose_name = "Historia"
        verbose_name_plural = "Historias"
        permissions = (
            ('historia', 'Can ALL historia'),
        )
    def _num(self):
        return "%s" % (self.id)

    def __str__(self):
        return "%s %s %s %s" % ("La mascota", self.mascota, "con N° Historia", self.num_historia)
