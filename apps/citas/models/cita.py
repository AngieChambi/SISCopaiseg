u"""Módulo Cita."""

from django.db import models
from .eventos import Evento
from apps.sad.models import User
from apps.clinica.models.cliente import Cliente


class Cita(models.Model):
    u"""Modelo Cita."""
    descripcion = models.TextField(blank=True)
    date = models.DateTimeField()
    estado = models.BooleanField(blank=True, default=True)
    evento = models.ForeignKey(
        Evento, verbose_name='Eventos frecuentes')
    veterinario = models.ForeignKey(
        User,)
    cliente = models.ForeignKey(Cliente)
    # veterinario = models.ForeignKey(
    #     Trabajador,
    #     limit_choices_to={'is_veterinario': True})

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta."""
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        """Str."""
        return '%s: %s' % (self.evento.title, self.descripcion)
