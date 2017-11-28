from django.conf.urls import url
from .views.trabajador import *

urlpatterns = [

    # ===================TRABAJADOR==========================
    # url(r'^trabajador/listar/$', TrabajadorListView.as_view(),
    #     name="trabajador_list"),
    # url(r'^trabajador/crear/$', TrabajadorCreateView.as_view(),
    #     name="trabajador_add"),
    url(r'^perfil/editar/$', TrabajadorUpdateView.as_view(),
        name="trabajador_upd"),
    # url(r'^trabajador/eliminar/(?P<pk>.*)/$', TrabajadorDeleteView.as_view(),
    #     name="trabajador_del"),
]
