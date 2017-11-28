u"""Módulo View especie."""
import json
import logging
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from django.views.generic import TemplateView
from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from apps.params.models import Person

from ..models.servicios import Servicios
from ..forms.servicios import ServiciosForm

log = logging.getLogger(__name__)


import json
from django.core import serializers


class ServiciosCreateView(CreateView):
    """  """
    model = Servicios
    form_class = ServiciosForm
    template_name = "configuracion/servicios/list_servicio.html"
    success_url = reverse_lazy("configuracion:servicios_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ServiciosCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ServiciosCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'servicios'
        context['object_list'] = Servicios.objects.all()
        context['title'] = ('Administrar %s') % ('Servicios')
        return context

    def get_form_kwargs(self):
        kwargs = super(ServiciosCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        self.object.veterinario = self.request.user
        print("===========//==============")
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(ServiciosCreateView, self).form_valid(form)


class ServiciosUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Servicios
    form_class = ServiciosForm
    template_name = "configuracion/servicios/list_servicio.html"
    success_url = reverse_lazy("configuracion:servicios_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Tipo Documento Create View dispatch."""

        return super(ServiciosUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(ServiciosUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['object_list'] = Servicios.objects.all()
        context['title'] = ('Administrar %s') % ('Servicios')
        return context

    def form_valid(self, form):
        """Tipo Documento Update View form_valid."""
        self.object = form.save(commit=False)

        msg = ('%(name)s "%(obj)s" fue cambiado satisfacoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(ServiciosUpdateView, self).form_valid(form)



class ServicioDeleteView(DeleteView):
    """Empresa Delete View."""

    model = Servicios
    success_url = reverse_lazy('configuracion:servicios_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Empresa Delete View dispatch."""
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(ServicioDeleteView,
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
