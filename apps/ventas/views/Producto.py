u"""Módulo View Departamento."""

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
from django.http import HttpResponse

from ..models.Producto import Producto
from ..forms.Producto import ProductoForm
from django.core import serializers
import logging
log = logging.getLogger(__name__)


class ProductoListView(ListView):
    u"""Tipo Documento Identidad."""

    model = Producto
    paginate_by = settings.PER_PAGE
    template_name = "ventas/inventario/Producto.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ProductoListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'nombre')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(ProductoListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Producto')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class ProductoCreateView(CreateView):
    u"""Tipo Documento Identidad."""

    model = Producto
    form_class = ProductoForm
    template_name = "ventas/inventario/formProducto.html"
    success_url = reverse_lazy("ventas:producto_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ProductoCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(ProductoCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'tipodoc'
        context['title'] = ('Agregar %s') % ('Producto')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        self.object.precioV = self.request.POST.get("precioV")
        self.object.precioC = self.request.POST.get("precioC")
        self.object.save()

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }

        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(ProductoCreateView, self).form_valid(form)


class ProductoUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Producto
    form_class = ProductoForm
    template_name = "ventas/inventario/formProducto.html"
    success_url = reverse_lazy("ventas:producto_list")

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

        return super(ProductoUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(ProductoUpdateView,
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
        return super(ProductoUpdateView, self).form_valid(form)

    def get_initial(self):
        context = super(ProductoUpdateView, self).get_initial()
        context = context.copy()
        context['fechaVencimiento'] = self.object.fechaVencimiento.strftime(
            "%Y-%m-%d")

        return context


class ProductoDeleteView(DeleteView):
    """Empresa Delete View."""

    model = Producto
    success_url = reverse_lazy('ventas:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Empresa Delete View dispatch."""
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'pro_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(ProductoDeleteView,
                     self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        u"""
        Empresa Delete View delte.

        Función para eliminar la empresa sobre un metodo que verifica las
        dependencias de que tiene la tabla mostrando un mensaje de validacion.
        """
        try:
            d = self.get_object()
            print(d.existencia)
            if d.existencia > 0.0:
                messages.warning(
                    self.request,
                    ('Este producto no se puede dar de baja, porque tiene %(existencias)s existencias') %
                    {
                        "existencias": d.existencia
                    })
            else:
                d.state = False if d.state else True
                d.save()
                messages.success(self.request, (
                    ' %(name)s "%(obj)s" fue cambiado satisfactorialmente.') % {
                    'name': capfirst(force_text(self.model._meta.verbose_name)),
                    'obj': force_text(d)
                })
            if not d.id:
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        """Empresa Delete View get."""
        return self.delete(request, *args, **kwargs)


def ProductoGetAjax(request):
    if request.is_ajax():
        con = Producto.objects.filter(
            nombre__icontains=request.GET['producto'],state=True)[:5]
        data = serializers.serialize(
            "json", con)

        return HttpResponse(data, content_type='application/json')
