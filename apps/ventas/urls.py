from django.conf.urls import *
from apps.ventas.views.main import *
from apps.ventas.views.Departamento import *
from apps.ventas.views.Categoria import *
from apps.ventas.views.Producto import *
from apps.ventas.views.UnidadMedida import *
from apps.ventas.views.Venta import *
from apps.ventas.views.VentaDetalle import *
from apps.clinica.views.vacunacionviews import get_drugs
from apps.clinica.views.colamedicaviews import  VentasView

urlpatterns = [
    # departamento
    url(r'^departamento/listar/$', DepartamentoListView.as_view(),
        name="departamento_list"),
    url(r'^departamento/crear/$', DepartamentoCreateView.as_view(),
        name="departamento_add"),
    url(r'^departamento/actualizar/(?P<pk>.*)/$',
        DepartamentoUpdateView.as_view(),
        name="departamento_upd"),
    url(r'^departamento/eliminar/(?P<pk>.*)/$',
        DepartamentoDeleteView.as_view(),
        name="departamento_del"),
    url(r'^departamento/crear/ajax/$', PostDepartamentoAjax,
        name="post_departamento_ajax"),
    # categoria
    url(r'^categoria/listar/$', CategoriaListView.as_view(),
        name="categoria_list"),
    url(r'^categoria/crear/$', CategoriaCreateView.as_view(),
        name="categoria_add"),
    url(r'^categoria/actualizar/(?P<pk>.*)/$', CategoriaUpdateView.as_view(),
        name="categoria_upd"),
    url(r'^categoria/eliminar/(?P<pk>.*)/$', CategoriaDeleteView.as_view(),
        name="categoria_del"),
    url(r'^categoria/crear/ajax/$', PostCategoriaAjax,
        name="post_categoria_ajax"),
    # categoria
    url(r'^producto/listar/$', ProductoListView.as_view(),
        name="producto_list"),
    url(r'^producto/crear/$', ProductoCreateView.as_view(),
        name="producto_add"),
    url(r'^producto/actualizar/(?P<pk>.*)/$', ProductoUpdateView.as_view(),
        name="producto_upd"),
    url(r'^producto/eliminar/(?P<pk>.*)/$', ProductoDeleteView.as_view(),
        name="producto_del"),

    # Unidad de medida
    url(r'^uni/listar/$', UnidadMedidaListView.as_view(),
        name="unidad_medida_list"),
    url(r'^uni/crear/$', UnidadMedidaCreateView.as_view(),
        name="unidad_medida_add"),
    url(r'^uni/actualizar/(?P<pk>.*)/$', UnidadMedidaUpdateView.as_view(),
        name="unidad_medida_upd"),
    url(r'^uni/eliminar/(?P<pk>.*)/$', UnidadMedidaDeleteView.as_view(),
        name="unidad_medida_del"),

    url(r'^reporte/venta/$', VentaListView.as_view(),
        name="reporte_ventas"),
    url(r'^reporte/venta/(?P<pk>\d+)/$', DetalleVentaListView.as_view(),
        name="detalle_go"),
    url(r'^uni/crear/ajax/$', PostUnidadAjax, name="post_unidad_ajax"),
    url(r'^univ/crear/ajax/$', PostUnidadVentasAjax,
        name="post_unidad_ventas_ajax"),
    url(r'^uni/cargarcarro/$', CrearCarroTemplateView,
        name="carro"),
    url(r'^uni/vendercarr/$', VenderCarro,
        name="vender_carro"),
    url(r'^cliente/filter/$', VentaAjaxCliente,
        name="detalle_ajax"),
    url(r'^date/filter/$', VentaAjaxDate,
        name="detalle_ajax_date"),

    # venta
    url(r'^venta/listar/$', VentaListView.as_view(),
        name="venta_list"),
    #   name="venta_add"),


    # Detallaventa
    url(r'^ventadetalle/listar/$', DetalleVentaListView.as_view(),
        name="ventadetalle_list"),
    # url(r'^ventadetalle/crear/$', DetalleVentaCreateView.as_view(),
    #  name="ventadetalle_add"),
    url(r'^producto/listar/ajax/$', ProductoGetAjax),

    # buscadores
    url(r'^producto/search/$', BuscarProducto, name='producto_s'),
    url(r'^cliente/search/$', get_drugs, name='get_cliente_venta'),


]
