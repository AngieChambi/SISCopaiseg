u"""Módulo View Categoria"""

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


from ..models.Categoria import Categoria
from ..forms.Categoria import CategoriaForm

import logging
log = logging.getLogger(__name__)
from django.shortcuts import render, HttpResponse
import json


def PostCategoriaAjax(request):
    if request.method == 'POST' and request.is_ajax():
        c = Categoria()
        c.descripcion = request.POST.get('des')
        c.departamento_id = request.POST.get('dep')
        c.save()
        cat = Categoria.objects.last()
        categoria_json = {}
        categoria_json['pk'] = cat.id
        categoria_json['name'] = cat.descripcion
        data_json = json.dumps(categoria_json)

    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')


class CategoriaListView(ListView):
    u"""Tipo Documento Identidad."""

    model = Categoria
    paginate_by = settings.PER_PAGE
    template_name = "ventas/inventario/Categoria.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(CategoriaListView,
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
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(CategoriaListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Categoria')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class CategoriaCreateView(CreateView):
    u"""Tipo Documento Identidad."""

    model = Categoria
    form_class = CategoriaForm
    template_name = "ventas/inventario/formCategoria.html"
    success_url = reverse_lazy("ventas:categoria_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(CategoriaCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(CategoriaCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'tipodoc'
        context['title'] = ('Agregar %s') % ('Categoria')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=True)

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }

        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(CategoriaCreateView, self).form_valid(form)


class CategoriaUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Categoria
    form_class = CategoriaForm
    template_name = "ventas/inventario/formCategoria.html"
    success_url = reverse_lazy("ventas:categoria_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Tipo Documento Create View dispatch."""
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'cat_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        return super(CategoriaUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(CategoriaUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Actualizar %s') % ('Categoria')
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
        return super(CategoriaUpdateView, self).form_valid(form)


class CategoriaDeleteView(DeleteView):
    """Empresa Delete View."""

    model = Categoria
    success_url = reverse_lazy('ventas:categoria_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Empresa Delete View dispatch."""
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'cat_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(CategoriaDeleteView,
                     self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        u"""
        Empresa Delete View delte.

        Función para eliminar la empresa sobre un metodo que verifica las
        dependencias de que tiene la tabla mostrando un mensaje de validacion.
        """
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
        """Empresa Delete View get."""
        return self.delete(request, *args, **kwargs)
