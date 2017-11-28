# coding: utf-8 _*_
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError

from smart_selects.db_fields import ChainedForeignKey

from ..models.cliente import Cliente
from apps.configuracion.models.especie import Especie, Raza, Color

CONDICION = (
    ('Buena', "Buena"),
    ('Regular', "Regular"),
    ('Demacrada', "Demacrada")
)

BOOL_GENERO = (
    ('Macho', "Macho"),
    ('Hembra', "Hembra")
)


class Mascota(models.Model):

    nombre = models.CharField(max_length=100)
    duenho = models.ForeignKey(Cliente, related_name='mascotas')
    fecha_nacimiento = models.DateTimeField(
        capfirst(_('Fecha Nacimiento')), null=True, blank=True)
    genero = models.CharField(
        max_length=10, choices=BOOL_GENERO, default='Macho')
    especie = models.ForeignKey(Especie, related_name='especie', max_length=100)
    raza = ChainedForeignKey(
		Raza,
		chained_field="especie",
		chained_model_field="especie",
		show_all=False,
		auto_choose=True,
        sort=True
	)
    color = ChainedForeignKey(
    	Color,
    	chained_field="raza",
    	chained_model_field="raza",
    	show_all=False,
    	auto_choose=True,
        sort=True
    )
    cond_corporal = models.CharField(
        max_length=10, choices=CONDICION, default='Buena')
    esterelizado = models.BooleanField(
        capfirst(_('Esterelizado...?')), default=True)
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    is_actived = models.BooleanField(_('Actived'), default=False)
    descripcion = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        permissions = (
            ('mascota', 'Can ALL mascota'),
            ('mascota_perfil', 'Can LIST perfil'),
        )

    def __str__(self):
        return "%s" % self.nombre
