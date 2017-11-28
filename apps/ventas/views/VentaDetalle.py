u"""Módulo View DetalleVenta"""

from backengo.utils.decorators import permission_resource_required


from django.conf import settings

from django.utils.decorators import method_decorator

from django.views.generic.list import ListView

from apps.ventas.models.Producto import Producto

from django.utils.text import capfirst

from ..models.Venta_Detalle import Detalle_Venta
from ..models.Venta import Venta
from django.core import serializers
from django.http import HttpResponse

import logging
log = logging.getLogger(__name__)


class DetalleVentaListView(ListView):
    u"""Tipo Documento Identidad."""

    model = Detalle_Venta
    paginate_by = settings.PER_PAGE
    template_name = "ventas/venta/DetalleVenta.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(DetalleVentaListView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(DetalleVentaListView, self).get_context_data(**kwargs)
        ventas = Venta.objects.get(id=self.kwargs['pk'])
        context['opts'] = self.model._meta
        context['detalle'] = Detalle_Venta.objects.filter(
            venta=ventas).order_by('pk')
        context['cantidad'] = context['detalle'].count()
        context['venta'] = ventas
        context['sub'] = ventas.total - ventas.igv
        return context


def VenderCarro(request):
    if request.is_ajax():
        data = "33333"
        print(request.GET['Venta'])
        # data = serializers.serialize(
        #     "json", Producto.objects.filter(id=request.GET['p']))
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')


def CrearCarroTemplateView(request):
    if request.is_ajax():
        data = serializers.serialize(
            "json", Producto.objects.filter(id=request.GET['p']))
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')
