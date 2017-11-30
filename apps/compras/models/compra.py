from django.db import models

from apps.compras.models.Proveedor import Proveedor
from apps.sad.models import User


class Compra(models.Model):

    fe_compra = models.DateTimeField('Fecha de compra',
                                     auto_now_add=True)
    # comprobante = models.ImageField(
    #     upload_to='comprobante_compra',
    #     verbose_name='Seleccione el archivo', blank=False, null=False)
    comprobante = models.ImageField(
        upload_to='persons', blank=True, null=True)
    total = models.DecimalField(
        'Total', max_digits=20, decimal_places=2, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor)
    usuario = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        permissions = (
            ('compra', 'Can ALL compra'),
        )

    def __str__(self):
        return "%s" % (self.id)
