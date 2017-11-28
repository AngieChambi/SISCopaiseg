u"""Módulo View Venta"""

from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.http import HttpResponse
import json
from decimal import Decimal
from math import ceil, floor
from ..models.Venta import Venta
from apps.clinica.models.cliente import Cliente
from ..models.Producto import Producto
from ..forms.Venta import VentaForm
from ..forms.Producto import ProductoForm
from ..models.Venta_Detalle import Detalle_Venta

from ..forms.VentaDetalle import Detalle_VentaForm

from django.db import transaction
import logging
log = logging.getLogger(__name__)


class MainCreateView(CreateView):
    u"""Tipo Documento Identidad."""

    model = Venta
    form_class = VentaForm
    template_name = "ventas/index.html"
    success_url = reverse_lazy("ventas:ventaslist",)

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(MainCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(MainCreateView,
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
            print("==============")
            venta = json.loads(self.request.POST.get('data_venta'))
            print("______________1_________________")
            print(venta)
            print(self.request.POST.get('cliente'))

            def float_round(num, places=0, direction=floor):
                return direction(num * (10**places)) / float(10**places)
            self.object.total = venta['total']
            self.object.igv = venta['igv']
            self.object.cliente_id = venta['cliente']
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

        #  self.object = form.save(commit=False)
        # sid = transaction.savepoint()
        # try:
        #     venta = json.loads(self.request.POST.get('data_venta'))
        #     print("______________1_________________")
        #     print(venta)
        #     print(self.request.POST.get('cliente'))
        #     self.object.total = venta['total']
        #     self.object.igv = venta['igv']
        #     self.object.save()
        #     for p in venta['productos']:
        #         dv = Detalle_Venta(
        #             producto_id=p['id'],
        #             venta=self.object,
        #             cantidad=p['cantidad'],
        #             # igv=p['igv'],
        #             importe=p['importe'],
        #         )
        #         dv.save()

        except Exception as e:
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
        return super(MainCreateView, self).form_valid(form)


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


# @transaction.atomic
# def facturaCrear(request):

#     form = None
#     if request.method == 'POST':
#         sid = transaction.savepoint()
#         try:
#             proceso = json.loads(request.POST.get('proceso'))
#             print proceso
#             if 'serie' not in proceso:
#                 msg = 'Ingrese serie'
#                 raise Exception(msg)

#             if 'numero' not in proceso:
#                 msg = 'Ingrese numero'
#                 raise Exception(msg)

#             if 'clienProv' not in proceso:
#                 msg = 'El cliente no ha sido seleccionado'
#                 raise Exception(msg)

#             if len(proceso['producto']) <= 0:
#                 msg = 'No se ha seleccionado ningun producto'
#                 raise Exception(msg)

#             total = 0

#             for k in proceso['producto']:
#                 producto = Producto.objects.get(id=k['serial'])
#                 subTotal = (producto.precio) * int(k['cantidad'])
#                 total += subTotal

#             crearFactura = Factura(
#                 serie=proceso['serie'],
#                 numero=proceso['numero'],

#                 cliente=Cliente.objects.get(id=proceso['clienProv']),
#                 fecha=timezone.now(),
#                 total=total,
#                 vendedor=request.user
#             )
#             crearFactura.save()
#             print "Factura guardado"
#             print crearFactura.id
#             for k in proceso['producto']:
#                 producto = Producto.objects.get(id=k['serial'])
#                 crearDetalle = DetalleFactura(
#                     producto=producto,
#                     descripcion=producto.nombre,
#                     precio = producto.precio,
#                     cantidad=int(k['cantidad']),
#                     impuesto=producto.igv* int(k['cantidad']),
#                     subtotal=producto.precio * int(k['cantidad']),
#                     factura = crearFactura
#                 )
#                 crearDetalle.save()

#             messages.success(
#                 request, 'La venta se ha realizado satisfactoriamente')
#         except Exception, e:
#             try:
#                 transaction.savepoint_rollback(sid)
#             except:
#                 pass
#             messages.error(request, e)

# return render_to_response('facturacion/crear_factura.html', {'form':
# form}, context_instance=RequestContext(request))


def BuscarProducto(request):
    if request.is_ajax:
        search = request.GET.get('term', '')

        productos = Producto.objects.filter(
            existencia__icontains=search,state=True)

        results = []
        for producto in productos:
            producto_json = {}
            producto_json['nombre'] = producto.nombre
            producto_json['cantidad'] = str(producto.existencia)
            producto_json['id'] = producto.id
            results.append(producto_json)

        data_json = json.dumps(results)

    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


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
