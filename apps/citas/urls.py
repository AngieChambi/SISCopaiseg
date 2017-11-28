from django.conf.urls import url
from .views.cita import *

urlpatterns = [
    # ===================CLIENTE==========================
    url(r'^$', CitaView.as_view(),
        name="cita_list"),
    url(r'^listar/$', GetCitaAjax, name="cita_list_get"),
    url(r'^eventos/listar/$', GetEventsAjax, name="evets_list_get"),
    url(r'^eventos/crear$', PostEventsAjax, name="evets_post"),
    url(r'^crear/$', CitaCreateView.as_view(),
        name="cita_add"),
    url(r'^mascota/crear/$', CitaMascotaCreateView.as_view(),
            name="cita_mascota_add"),
    url(r'^actualizar/(?P<pk>.*)/$', CitaUpdateView.as_view(),
        name="cita_upd"),
    url(r'^eliminar/(?P<pk>.*)/$', CitaDeleteView.as_view(),
        name="cita_del"),
]
