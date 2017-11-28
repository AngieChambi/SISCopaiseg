from django.contrib import admin

# Register your models here.
from .models.eventos import Evento
from .models.cita import Cita

admin.site.register(Evento)
admin.site.register(Cita)
