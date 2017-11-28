u"""Módulo View Venta"""

from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.text import capfirst
from django.views.generic.list import ListView
import json

from ..models.Venta import Venta
import datetime
import logging
log = logging.getLogger(__name__)


class VentaListView(ListView):
    u"""Tipo Documento Identidad."""

    model = Venta
    template_name = "ventas/venta/Reporte.html"
    context_object_name = 'ventas'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(VentaListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""

        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'fechav')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """

        context = super(VentaListView,
                        self).get_context_data(**kwargs)
        print(context)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Reporte de %s del día'
                            ) % capfirst('Venta')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


def VentaAjaxCliente(request):
    if request.is_ajax():
        print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"+request.GET['id'])



        cliente = Venta.objects.filter(cliente=request.GET['id'])
        print(cliente)
        results = []
        for i in range(cliente.count()):
            print(i)
            producto_json = {}
            producto_json['id'] = cliente[i].id
            producto_json['igv'] = str(cliente[i].igv)
            producto_json['fecha'] = str(cliente[i].fechav)
            producto_json['usuario'] = cliente[i].user_id
            producto_json['cliente'] = str(cliente[i].cliente)
            producto_json['total'] = str(cliente[i].total)
            results.append(producto_json)
            print(results)
        data_json = json.dumps(results)

        return HttpResponse(data_json)
    else:
        return redirect('/reporte/venta/')


def VentaAjaxDate(request):
    if request.is_ajax():
        m = str(request.GET['fechav'])
        ven = Venta.objects.filter(
            fechav=datetime.datetime.strptime(m, "%Y-%m-%d").date())
        print(m)
        print(ven)
        results = []
        for i in range(ven.count()):
            print(i)
            producto_json = {}
            producto_json['id'] = ven[i].id
            producto_json['igv'] = str(ven[i].igv)
            producto_json['fecha'] = str(ven[i].fechav)
            producto_json['usuario'] = ven[i].user_id
            producto_json['cliente'] = str(ven[i].cliente)
            producto_json['total'] = str(ven[i].total)
            results.append(producto_json)
            print(results)
        data_json = json.dumps(results)

        return HttpResponse(data_json)
    else:
        return redirect('/reporte/venta/')
