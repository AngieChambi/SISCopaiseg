u"""Módulo View Tipo Documento."""

from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
import json

from ..models.Proveedor import Proveedor
from ..forms.Proveedor import ProveedorForm

import logging
log = logging.getLogger(__name__)


def GetProveedorAjax(request):
    if request.method == 'GET' and request.is_ajax():
        cat = Proveedor.objects.get(id=request.GET.get('pk'))
        proveedor_json = {}
        proveedor_json['pk'] = cat.id
        proveedor_json['tipodoc'] = cat.tipodoc
        proveedor_json['numdoc'] = cat.numdoc
        proveedor_json['razon_social'] = cat.razon_social
        proveedor_json['representante_legal'] = cat.representante_legal
        proveedor_json['direccion'] = cat.direccion
        proveedor_json['telefono'] = cat.telefono
        proveedor_json['email'] = cat.email
        proveedor_json['estado'] = cat.estado
        data_json = json.dumps(proveedor_json)

    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')


def PostProveedorAjax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = Proveedor()
            d.razon_social = request.POST.get('rs')
            d.tipodoc = request.POST.get('td')
            d.numdoc = request.POST.get('nd')
            d.representante_legal = request.POST.get('rs')
            d.direccion = request.POST.get('d')
            d.telefono = request.POST.get('t')
            d.email = request.POST.get('e')
            # if request.GET.get('q'):
            #     d.enti_bancaria = request.POST.get('c')
            # if request.GET.get('q'):
            #     d.num_cuenta = request.POST.get('nc')
            d.save()
            obj = Proveedor.objects.last()
            unidad_json = {}
            unidad_json['pk'] = obj.id
            unidad_json['name'] = '%s %s' % (obj.numdoc, obj.razon_social)
            data_json = json.dumps(unidad_json)
        except Exception as e:
            data_json = '{"data":"fail"}'
            print(e)
    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')


class ProveedorListView(ListView):
    u"""Tipo Documento Identidad."""

    model = Proveedor
    paginate_by = settings.PER_PAGE
    template_name = "compras/proveedor/index.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ProveedorListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'razon_social')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(ProveedorListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Proveedor')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class ProveedorCreateView(CreateView):
    u"""Tipo Documento Identidad."""

    model = Proveedor
    form_class = ProveedorForm
    template_name = "compras/proveedor/form.html"
    success_url = reverse_lazy("compras:proveedor_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ProveedorCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(ProveedorCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'tipodoc'
        context['title'] = ('Agregar %s') % ('Proveedor')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=True)
        self.object.representante_legal = form.cleaned_data['razon_social']

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }

        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(ProveedorCreateView, self).form_valid(form)


class ProveedorUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Proveedor
    form_class = ProveedorForm
    template_name = "compras/proveedor/form.html"
    success_url = reverse_lazy("compras:proveedor_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Tipo Documento Create View dispatch."""
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'doc_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        return super(ProveedorUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(ProveedorUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Actualizar %s') % ('Proveedor')
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
        return super(ProveedorUpdateView, self).form_valid(form)


class ProveedorDeleteView(DeleteView):
    """Empresa Delete View."""

    model = Proveedor
    success_url = reverse_lazy('compras:proveedor_list')

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
        return super(ProveedorDeleteView,
                     self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        u"""
        Empresa Delete View delte.

        Función para eliminar la empresa sobre un metodo que verifica las
        dependencias de que tiene la tabla mostrando un mensaje de validacion.
        """
        try:
            d = self.get_object()
            d.estado = False if d.estado else True
            d.save()
            msg = _(
                ' %(name)s "%(obj)s" fue cambiado satisfactorialmente.') % {
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
        """Empresa Delete View get."""
        return self.delete(request, *args, **kwargs)
