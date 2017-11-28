u"""Módulo Evento."""

from django.db import models


class Evento(models.Model):
    u"""Modelo Evento."""

    title = models.CharField(max_length=100)
    color = models.CharField(max_length=24)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta."""
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        """Str."""
        return "%s" % self.title
