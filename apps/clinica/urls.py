from django.conf.urls import url


from .views.atencionviews import AtencionHistoriaListView, AtencionListView, AtencionCreateView, AtencionTerminadaView
from .views.colamedicaviews import ColaMedicaListView,MainCreateView, ColaMedicaDeleteView, ColasMedicasListView, BuscarCliente
from .views.vacunacionviews import  get_drugs, BuscarProducto
from .views.consulta_diagnostico import  get_diagnosticos
from .views.tratamientos import  get_tratamientos
from .views.consulta_pruebas_auxiliares import  get_pruebas_auxiliares
from .views.historiaviews import HistoriasListView, HistoriaFichaListView,  HistoriaMascotaDetailView, HistoriaMascotaCreateView
from .views.mascotaviews import MascotaListView, MascotaCreateView, MascotaPerfilView, MascotaHistoriaListView, MascotaUpdateView, MascotaUpdateActiveView
from .views.cliente import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView, PostClienteAjax
from .views.cunsulta import ConsultaCreateView, ConsultaUpdateView,  ConsultaDeleteView
from .views.notas import NotasCreateView, upload, upload_delete
from .views.vacunacion import VacunacionCreateView, PostVacunacionAjax
from .views.colamedicaviews import MainCreateView,VentasView
urlpatterns = [
    url(r'^api/get_drugs/', get_drugs, name='get_drugs'),
    url(r'^api/diagnostico/', get_diagnosticos, name='get_diagnosticos'),
    url(r'^api/pruebas_auxiliares/', get_pruebas_auxiliares, name='get_pruebas_auxiliares'),
    url(r'^api/tratamientos/', get_tratamientos, name='get_tratamientos'),

    #BUSQUEDAS-URLS

    url(r'^producto/search/',
        BuscarProducto, name='search_producto_recepcion'),
    url(r'^cliente/search/',BuscarCliente, name='search_cliente'),



#Atencion Medica
    url(r'^atenciones/listar/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)$', AtencionListView.as_view(), name="historia_list"),
    url(r'^atenciones/historia/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)$', AtencionHistoriaListView.as_view(), name="atencion_historia_list"),
    url(r'^atenciones/crear/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)/$', AtencionCreateView.as_view(), name="atenciones_add"),
    url(r'^atencion/terminada/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        AtencionTerminadaView.as_view(), name='atencion_satate'),

#Consultas
    url(r'^atencion/consulta/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)$', ConsultaCreateView.as_view(), name='consulta_add'),
    url(r'^atencion/consulta/editar/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)/(?P<atencion_pk>[^/]+)/(?P<pk>.*)/$', ConsultaUpdateView.as_view(), name='consulta_update'),
    url(r'^atencion/consulta/eliminar/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)/(?P<pk>.*)/$', ConsultaDeleteView.as_view(), name="consulta_delete"),

    #Notas
    url(r'^atencion/notas/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)/(?P<atencion_pk>[^/]+)/$', NotasCreateView.as_view(), name='nota_add'),

    #Archivos

    #Vacunacion
    url(r'^atencion/vacunacion/(?P<mascota_pk>[^/]+)/(?P<colamedica_pk>[^/]+)/$', VacunacionCreateView.as_view(), name='vacuna_add'),
    url(r'^atencion/vacunacion/crear-ajax/$', PostVacunacionAjax, name="post_vacunacion_ajax"),

    #Cola Medica
    url(r'^colamedica/listar/$', ColaMedicaListView.as_view(), name="listar_medica"),
    url(r'^colamedica/lista/$', ColasMedicasListView.as_view(), name="lista_medica"),

    url(r'^colamedica/crear/$', MainCreateView.as_view(), name="crear_medica"),
    url(r'^ventas/$', VentasView.as_view(), name="crear_venta"),
    url(r'^colamedica/eliminar/(?P<pk>.*)/$', ColaMedicaDeleteView.as_view(), name="eliminar_medica"),

    #url(r'^colamedica/detail/(?P<pk>.*)/$', AtencionMedicaView.as_view(), name='colamedica_detail'),



    # Historia
    url(r'^historia/listar/$', HistoriasListView.as_view(), name="listar_historia"),
    url(r'^historia/ficha/(?P<mascota_pk>[^/]+)$', HistoriaFichaListView.as_view(), name="ver_ficha_clinica"),
    url(r'^historia/crear/(?P<cliente_pk>[^/]+)/(?P<mascota_pk>[^/]+)$',
        HistoriaMascotaCreateView.as_view(), name='crear_historia'),
    url(r'^historia/detail/(?P<pk>.*)/$',
        HistoriaMascotaDetailView.as_view(), name='historia_detail'),

    # Mascota
    url(r'^mascota/listar/(?P<cliente_pk>[^/]+)$',
        MascotaListView.as_view(), name="mascota_list"),
    url(r'^mascota/crear/(?P<cliente_pk>[^/]+)$',
        MascotaCreateView.as_view(), name="mascota_add"),
    url(r'^mascota/actualizar/(?P<pk>.*)/$',
        MascotaUpdateView.as_view(), name="actualizar_mascota"),
    url(r'^mascota/state/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        MascotaUpdateActiveView.as_view(), name='mascota-state'),
    url(r'^mascota/perfil/(?P<pk>.*)/$', MascotaPerfilView.as_view(), name="mascota_perfil_list"),
    url(r'^mascota/historia/(?P<mascota_pk>[^/]+)/$', MascotaHistoriaListView.as_view(), name="historia_list"),
    # ===================CLIENTE==========================
    url(r'^cliente/listar/$', ClienteListView.as_view(), name="cliente_list"),
    url(r'^cliente/crear/$', ClienteCreateView.as_view(), name="cliente_add"),
    url(r'^cliente/actualizar/(?P<pk>.*)/$',
        ClienteUpdateView.as_view(), name="cliente_upd"),
    url(r'^cliente/eliminar/(?P<pk>.*)/$',
        ClienteDeleteView.as_view(), name="cliente_del"),
    url(r'^cliente/crear/ajax$', PostClienteAjax, name="post_cliente_ajax"),
]
