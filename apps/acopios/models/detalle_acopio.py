from django.db import models
from ..models.parcela import Parcela
from ..models.acopio import Acopio


class DetalleAcopio(models.Model):
    parcela = models.ForeignKey(Parcela, on_delete=models.CASCADE)
    acopio = models.ForeignKey(Acopio)
    kilos = models.DecimalField(max_digits=20, decimal_places=2)
    precio_uni = models.DecimalField(
        'Precio Unitario', max_digits=20, decimal_places=2)
    total_pagar = models.DecimalField(
        'Precio a Pagar', max_digits=20, decimal_places=2, blank=True, null=True)
    # total_importe = models.aggregate(Sum('importe'))

    class Meta:
        verbose_name = "Detalle  Acopio"
        verbose_name_plural = "Detalles Acopio"

    def __str__(self):
        return "%s %s %s" % (self.acopio.socio.persona.first_name,
                             self.acopio.socio.persona.last_name,
                             self.parcela.codigo)

    def _get_importe(self):
        return self.precio_uni * self.total_pagar
    importe = property(_get_importe)
