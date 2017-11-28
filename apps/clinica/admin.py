#encoding: utf-8
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

# models
from .models.colamedica import ColaMedica
from .models.mascota import Mascota
from .models.consulta import HallasgosClinicos, Diagnostico, Pruebas, Tratamiento
from .models.historia import Historial
from .models.atencion import Atencion
from .models.atenciones import Atenciones, ArchivosAdjuntos
from .models.vacunacion import Vacunacion
from .models.nota import Notas
from .models.cliente import Cliente
from .models.consulta_diagnostico import ConsultaDiagnostico

class HistoriaAdmin(admin.ModelAdmin):
    model = Historial
    search_fields = ('num_historia',)
    list_display = ('num_historia','mascota','get_duenho','created_ath', 'get_direccion','get_ciudad', 'get_telefono','get_especie','get_raza', 'get_color','get_sexo', 'get_edad', )

    def get_direccion(self, obj):
        return obj.mascota.duenho.direccion
    get_direccion.admin_order_field  = 'mascota'  #Allows column order sorting
    get_direccion.short_description = 'Direccion'

    def get_duenho(self, obj):
        return obj.mascota.duenho
    get_duenho.admin_order_field  = 'mascota'  #Allows column order sorting
    get_duenho.short_description = 'Dueño'

    def get_telefono(self, obj):
        return obj.mascota.duenho.telefono
    get_telefono.admin_order_field  = 'dueño'  #Allows column order sorting
    get_telefono.short_description = 'Telefono'

    def get_ciudad(self, obj):
        return obj.mascota.duenho.ciudad
    get_ciudad.admin_order_field  = 'mascota'  #Allows column order sorting
    get_ciudad.short_description = 'Ciudad'

    def get_especie(self, obj):
        return obj.mascota.especie
    get_especie.admin_order_field  = 'mascota'  #Allows column order sorting
    get_especie.short_description = 'Especie'

    def get_raza(self, obj):
        return obj.mascota.raza
    get_raza.admin_order_field  = 'mascota'  #Allows column order sorting
    get_raza.short_description = 'Raza'

    def get_color(self, obj):
        return obj.mascota.color
    get_color.admin_order_field  = 'mascota'  #Allows column order sorting
    get_color.short_description = 'Color'

    def get_sexo(self, obj):
        return obj.mascota.genero
    get_sexo.admin_order_field  = 'mascota'  #Allows column order sorting
    get_sexo.short_description = 'Sexo'

    def get_edad(self, obj):
        return obj.mascota.fecha_nacimiento
    get_edad.admin_order_field  = 'mascota'  #Allows column order sorting
    get_edad.short_description = 'Edad'


class ColaMedicaAdmin(admin.ModelAdmin):
    model = ColaMedica
    search_fields = ()
    list_display = ('fecha','descripcion','medico',)

class AtencionAdmin(admin.ModelAdmin):
    model = Atencion





admin.site.register(Atenciones)
admin.site.register(ArchivosAdjuntos)
admin.site.register(Mascota)
admin.site.register(Notas)
admin.site.register(Vacunacion)
admin.site.register(ColaMedica, ColaMedicaAdmin)
admin.site.register(Diagnostico)
admin.site.register(HallasgosClinicos)
admin.site.register(Pruebas)
admin.site.register(Tratamiento)
admin.site.register(Historial, HistoriaAdmin)
admin.site.register(Atencion, AtencionAdmin)

admin.site.register(Cliente)
admin.site.register(ConsultaDiagnostico)
