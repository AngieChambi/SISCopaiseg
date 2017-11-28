from django.conf.urls import url

from apps.configuracion.views.antiparasitarios import AntiparasitarioCreateView, AntiparasitarioListView, \
    AntiparasitarioUpdateView, AntiparasitarioDeleteView
from .views.especie import (EspecieAdministrarView, EspecieListView, RazaListView, ColorListView, PostEspecieAjax,
                            PostRazaAjax, PostColorAjax, EspecieUpdateView, EspecieDeleteView)
from .views.servicios import ServiciosCreateView, ServiciosUpdateView, ServicioDeleteView

urlpatterns = [
    url(r'^especie/listar/$', EspecieListView.as_view(), name="especie_list"),
    url(r'^raza/listar/(?P<especie_pk>[^/]+)$', RazaListView.as_view(), name="raza_list"),
    url(r'^color/listar/(?P<especie_pk>[^/]+)/(?P<raza_pk>[^/]+)$', ColorListView.as_view(), name="color_list"),

    url(r'^especie/administrar/$', EspecieAdministrarView.as_view(), name="especie_administrar"),

    url(r'^especie/crear-ajax/$', PostEspecieAjax, name="post_especie_ajax"),
    url(r'^raza/crear-ajax/$', PostRazaAjax, name="post_raza_ajax"),
    url(r'^color/crear-ajax/$', PostColorAjax, name="post_color_ajax"),

    url(r'^especie/actualizar/(?P<pk>.*)/$', EspecieUpdateView.as_view(), name="especie_upd"),
    url(r'^especie/eliminar/(?P<pk>.*)/$', EspecieDeleteView.as_view(), name="especie_del"),

    # Servicios
    url(r'^servicios/listar/$', ServiciosCreateView.as_view(), name="servicios_list"),
    url(r'^servicios/actualizar/(?P<pk>.*)/$', ServiciosUpdateView.as_view(), name="servicios_update"),
    url(r'^servicios/eliminar/(?P<pk>.*)/$', ServicioDeleteView.as_view(), name="servicios_delete"),
    # Antiparasitarios
    url(r'^antiparasitario/adminitrar/$', AntiparasitarioListView.as_view(), name="antiparasitario_admin"),
    url(r'^antiparasitario/crear/(?P<especie_pk>[^/]+)/$', AntiparasitarioCreateView.as_view(),
        name="antiparasitario_create"),
    url(r'^antiparasitario/actualizar/(?P<pk>.*)/$', AntiparasitarioUpdateView.as_view(), name="antiparasitario_update"),
    url(r'^antiparasitario/eliminar/(?P<pk>.*)/$', AntiparasitarioDeleteView.as_view(), name="antiparasitario_delete"),

]
