# -*- coding: utf-8 -*-
from django.db import models

Tipo_Documento = (
    ('RUC', 'Registro Único de Comprobante'),
    ('DNI', 'Documento nacional de Identidad'),
)


class Proveedor(models.Model):
    tipodoc = models.CharField('Tipo de Documento', max_length=30,
                               choices=Tipo_Documento,
                               default='Registro Único de Comprobante')
    numdoc = models.IntegerField('Número de documento')
    razon_social = models.CharField(
        'Razon social', max_length=50, blank=True, null=True)
    representante_legal = models.CharField(
        'Representante legal', max_length=50, blank=True, null=True)
    direccion = models.CharField('Direccion', max_length=30)
    telefono = models.IntegerField(
        'Telefono', blank=True, null=True)
    email = models.EmailField('Email', max_length=30, blank=True, null=True)
    enti_bancaria = models.CharField(
        'Entidad bancaria', max_length=30, blank=True, null=True)
    num_cuenta = models.IntegerField(
        'Número de cuenta',  blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        permissions = (
            ('proveedor', 'Can ALL proveedor'),
        )

    def __str__(self):
        return "%s %s" % (self.numdoc, self.razon_social)
