from django.db import models

from apps.clinica.models.cliente import Cliente
from apps.sad.models import User


class Venta(models.Model):
    codigo = models.CharField(max_length=50)
    fechav = models.DateField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    igv = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        permissions = (
            ('venta', 'Can ALL venta'),
        )

    def __str__(self):
        return "%s" % (self.codigo)
