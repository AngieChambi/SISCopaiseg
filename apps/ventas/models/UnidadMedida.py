from django.db import models


class UnidadMedidaV(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    simbolo = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Unidad de medida Venta"
        verbose_name_plural = "Unidad de medidas Ventas"

    def __str__(self):
        return self.nombre


class UnidadMedidaC(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    simbolo = models.CharField(max_length=10)
    cant_equivalencia = models.DecimalField(
        max_digits=20, decimal_places=2,
        verbose_name='Cantidad de equivalencia')
    unidad_medida_venta = models.ForeignKey(
        UnidadMedidaV,
        verbose_name='Unidad de medida para ventas')

    class Meta:
        verbose_name = "Unidad de medida Compra"
        verbose_name_plural = "Unidad de medidas Compras"

    def __str__(self):
        return ('1 %s a %s %s') % (self.nombre,
                                   self.cant_equivalencia,
                                   self.unidad_medida_venta.nombre)
