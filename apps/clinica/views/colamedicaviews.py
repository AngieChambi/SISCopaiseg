from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from ..forms.colamedicaform import ColaMedicaForm
from decimal import Decimal
from math import ceil, floor
from ..models.colamedica import ColaMedica
from apps.clinica.models.cliente import Cliente
from ..models.mascota import Mascota
from apps.ventas.models.Venta import Venta
from apps.ventas.forms.Venta import VentaForm
from apps.ventas.forms.Producto import ProductoForm
from apps.ventas.models.Producto import Producto

from apps.ventas.models.Venta_Detalle import Detalle_Venta
from django.db import transaction
import datetime
import logging
import json
log = logging.getLogger(__name__)

# Create your views here.


class ColasMedicasListView(ListView):
    model = ColaMedica
    paginate_by = settings.PER_PAGE
    template_name = "clinica/listasmedicas.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ColasMedicasListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'descripcion')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(ColasMedicasListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Pacientes en  %s de atencion'
                            ) % capfirst(' espera')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class ColaMedicaListView(ListView):
    model = ColaMedica
    paginate_by = settings.PER_PAGE
    template_name = "clinica/colamedica.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""

        idmascota = request.GET.get('id')
        print("holaass", idmascota)
        return super(ColaMedicaListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'descripcion')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(ColaMedicaListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Pacientes en  %s de atencion'
                            ) % capfirst(' espera')
        context['fecha'] = ColaMedica.objects.filter(
            fecha=datetime.date.today() ).order_by('fecha')
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        context['cantidad'] = context['fecha'].count()
        return context

##model = ColaMedica
  ##  form_class = ColaMedicaForm
    ##template_name = "clinica/busqueda.html"
    ##success_url = reverse_lazy("clinica:crear_medica")


class MainCreateView(CreateView):

    model = ColaMedica
    form_class = ColaMedicaForm
    template_name = "clinica/busqueda.html"
    success_url = reverse_lazy("clinica:crear_medica")

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(MainCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MainCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'tipodoc'
        context['title'] = ('Recepción')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }

        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(MainCreateView, self).form_valid(form)


class VentasView(CreateView):
    u"""Tipo Documento Identidad."""

    model = Venta
    form_class = VentaForm
    template_name = "clinica/ventas/index.html"  # "ventas/index.html"
    #success_url = reverse_lazy("ventas:ventaslist",)
    success_url = reverse_lazy("clinica:crear_medica")

    #@method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(VentasView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(VentasView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'tipodoc'
        context['title'] = ('Agregar %s') % ('Venta')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        sid = transaction.savepoint()
        print("______________0_________________")
        try:
            print(self.request.POST.get(''))
            print("======//////////////////========")
            print('data_venta' in self.request.POST.keys())
            venta = json.loads(self.request.POST.get('data_venta'))
            print("______________1_________________")
            print(venta)
            print(self.request.POST.get('cliente'))
            cantidadVenta=Venta.objects.all().count()

            def float_round(num, places=0, direction=floor):
                return direction(num * (10**places)) / float(10**places)
            self.object.total = venta['total']
            self.object.igv = venta['igv']
            self.object.cliente_id = venta['cliente']
            self.object.codigo = str(''.join((8 - len(str(cantidadVenta))) * ["0"])) + str(cantidadVenta+1)
            self.object.save()

            for p in venta['productos']:

                producto = Producto.objects.get(pk=p['id'])
                producto.existencia = producto.existencia - int(p['cantidad'])
                producto.MontoReal = float_round(
                    producto.MontoReal - (Decimal(p['importe']) - Decimal(p['importe'] * 0.18)), 2, ceil)

                producto.igv = float_round(
                    producto.igv - Decimal(p['igvp']), 2, ceil)
                print(producto.igv)
                producto.save()
                # producto.cantidad = producto.cantidad + int(p['cantidad'])
                # print(producto)
                # producto.update()
                dv = Detalle_Venta(
                    producto_id=p['id'],
                    venta=self.object,
                    cantidad=p['cantidad'],
                    # igv=p['igv'],
                    importe=p['importe'],
                )
                dv.save()
                print("__________________", dv)

        except Exception as e:
            print("ERRRRRRRRRRRRRRRRRRRRRRRR", e)
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(self.request, e)

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }

        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(VentasView, self).form_valid(form)


class VentaProductoUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Producto
    form_class = ProductoForm
    template_name = "ventas/index.html"
    success_url = reverse_lazy("ventas:ventaslist")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Tipo Documento Create View dispatch."""
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'pro_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        return super(VentaProductoUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(VentaProductoUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Actualizar %s') % ('Producto')
        return context

    def form_valid(self, form):
        """Tipo Documento Update View form_valid."""
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user

        msg = ('%(name)s "%(obj)s" fue cambiado satisfacoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(VentaProductoUpdateView, self).form_valid(form)


def BuscarCliente(request):
    if request.is_ajax:
        search = request.GET.get('term', '')

        clientes = Cliente.objects.filter(
            direccion__icontains=search)[:100]

        results = []
        for cliente in clientes:
            producto_json = {}
            producto_json['id'] = cliente.id
            producto_json['persona'] = str(cliente.persona)
            producto_json['direccion'] = cliente.direccion
            producto_json['ciudad'] = cliente.ciudad
            producto_json['telefono'] = cliente.telefono
            producto_json['email'] = cliente.email
            producto_json['documento'] = cliente.persona.identity_num
            results.append(producto_json)

        data_json = json.dumps(results)

    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


class ColaMedicaDeleteView(DeleteView):
    """Empresa Delete View."""

    model = ColaMedica
    success_url = reverse_lazy('clinica:listar_medica')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Empresa Delete View dispatch."""
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'doc_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(ColaMedicaDeleteView,
                     self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(
                    self.request,
                    ('No se puede Eliminar %(name)s') %
                    {
                        "name": capfirst(force_text(
                            self.model._meta.verbose_name)
                        ) + ' "' + force_text(d) + '"'
                    })
                raise Exception(msg)

            d.delete()
            msg = _(
                ' %(name)s "%(obj)s" fuel eliminado satisfactorialmente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
