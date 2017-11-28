# Register your models here.
from django.contrib import admin

from .models.Proveedor import Proveedor
from .models.compra import Compra
from .models.detallecompra import DetalleCompra

admin.site.register(Proveedor)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
