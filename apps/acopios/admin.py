from django.contrib import admin
from .models.socio import Socio
from .models.parcela import Parcela
from .models.acopio import Acopio
from .models.detalle_acopio import DetalleAcopio

# Register your models here.

admin.site.register(Socio)
admin.site.register(Parcela)
admin.site.register(Acopio)
admin.site.register(DetalleAcopio)
