from django.db import models

from apps.ventas.models.Producto import Producto
from apps.compras.models.compra import Compra


class DetalleCompra(models.Model):

    cantidad = models.PositiveIntegerField('Cantidad')
    precio_total = models.DecimalField(
        'Precio Total', max_digits=20, decimal_places=2)
    producto = models.ForeignKey(Producto)
    compra = models.ForeignKey(Compra)

    class Meta:
        verbose_name = "Detalle Compra"
        verbose_name_plural = "Detalles Compra"
        permissions = (
            ('detallecompra', 'Can ALL detallecompra'),
        )
    def __str__(self):
        return "%s" % (self.producto)
