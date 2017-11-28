from django.conf.urls import url
from apps.compras.views.Proveedor import *
from apps.compras.views.compra import *
from apps.compras.views.detallecompra import DetalleCompraListView
urlpatterns = [
    # Proveedor
    url(r'^proveedor/listar/$', ProveedorListView.as_view(),
        name="proveedor_list"),
    url(r'^proveedor/crear/$', ProveedorCreateView.as_view(),
        name="proveedor_add"),
    url(r'^proveedor/actualizar/(?P<pk>.*)/$',
        ProveedorUpdateView.as_view(), name="proveedor_upd"),
    url(r'^proveedor/eliminar/(?P<pk>.*)/$',
        ProveedorDeleteView.as_view(), name="proveedor_del"),
    url(r'^proveedor/get/ajax/$', GetProveedorAjax,
        name="get_proveedor_ajax"),
    url(r'^proveedor/crear/ajax/$', PostProveedorAjax,
        name="post_proveedor_ajax"),

    # Compra
    url(r'^compra/listar/$', CompraListView.as_view(),  name="compra_list"),
    url(r'^compra/crear/$', CompraCreateView.as_view(), name="compra_add"),
    url(r'^compra/actualizar/(?P<pk>.*)/$',
        CompraUpdateView.as_view(), name="compra_upd"),
    url(r'^detalle-compra/listar/(?P<id>\d+)/$',
        DetalleCompraListView.as_view(),  name="detallecompra_detail"),

]
