from django.contrib import admin

# Register your models here.
from .models.especie import Especie, Raza, Color, prueba
from .models.antiparasitarios import Antiparasitario
from .models.servicios import Servicios
from .models.vacunas import Vacunas

admin.site.register(Antiparasitario)
admin.site.register(Servicios)
admin.site.register(Vacunas)
admin.site.register(Especie)
admin.site.register(Raza)
admin.site.register(Color)
admin.site.register(prueba)
