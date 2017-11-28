# -*- coding: utf-8 -*-
u"""Módulo Cliente."""

from django.db import models
from apps.params.models import Person


class Cliente(models.Model):
    u"""Modelo Cliente."""
    persona = models.OneToOneField(Person)
    direccion = models.CharField(max_length=50, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    email = models.EmailField('E-mail', blank=True)
    telefono = models.IntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta."""
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        permissions = (
            ('cliente', 'Can ALL cliente'),
        )
    def __str__(self):
        """Str."""
        return "%s %s" % (self.persona.first_name, self.persona.last_name)
