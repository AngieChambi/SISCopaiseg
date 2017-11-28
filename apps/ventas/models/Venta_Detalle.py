from django.db import models

from ..models.Producto import Producto
from ..models.Venta import Venta


class Detalle_Venta(models.Model):
    producto = models.ForeignKey(Producto)
    venta = models.ForeignKey(Venta)
    cantidad = models.IntegerField()
    importe = models.DecimalField(decimal_places=2, max_digits=20)

    class Meta:
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalles Venta'
        permissions = (
            ('detalle_venta', 'Can ALL detalle_venta'),
        )
    def __str__(self):
        return "%s %s %s" % (self.venta.cliente.persona.first_name,
                             self.venta.cliente.persona.last_name,
                             self.producto.nombre)
