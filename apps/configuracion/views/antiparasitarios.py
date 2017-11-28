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

from apps.configuracion.forms.antiparasitarios import AntiparasitarioForm
from apps.configuracion.models.antiparasitarios import Antiparasitario
from apps.configuracion.models.especie import Especie
from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from apps.params.models import Person

log = logging.getLogger(__name__)

import json
from django.core import serializers


class AntiparasitarioListView(CreateView):
    u"""Servicios."""
    model = Antiparasitario
    form_class = AntiparasitarioForm
    template_name = "configuracion/antiparasitario/lista_antiparasitario.html"
    success_url = reverse_lazy("configuracion:antiparasitario_admin")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(AntiparasitarioListView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        """
        context = super(AntiparasitarioListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['object_list'] = Especie.objects.all()
        context['title'] = ('Seleccione %s para editar'
                            ) % capfirst('especie')
        print ("ggggggggggggggg", self.kwargs.get("especie_pk"))
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        self.object.especie_id = form.cleaned_data['especie']
        print("===========//==============")
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(AntiparasitarioListView, self).form_valid(form)


class AntiparasitarioCreateView(CreateView):
    """  """
    model = Antiparasitario
    form_class = AntiparasitarioForm
    template_name = "configuracion/antiparasitario/antiparasitario_add.html"
    success_url = reverse_lazy("configuracion:antiparasitario_admin")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AntiparasitarioCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AntiparasitarioCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'antiparasitarios'
        context['anti_list'] = Antiparasitario.objects.filter(especie__id=self.kwargs.get("especie_pk"))
        context['title'] = _('Add %s') % capfirst(_('antiparasitario'))

        print ("ggggggggggggggg", self.kwargs.get("especie_pk"))
        return context

    def get_form_kwargs(self):
        kwargs = super(AntiparasitarioCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class AntiparasitarioUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Antiparasitario
    form_class = AntiparasitarioForm
    template_name = "configuracion/antiparasitario/lista_antiparasitario.html"
    success_url = reverse_lazy("configuracion:antiparasitario_admin")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Tipo Documento Create View dispatch."""

        return super(AntiparasitarioUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(AntiparasitarioUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['anti_list'] = Antiparasitario.objects.all()
        context['title'] = ('Administrar %s') % ('Antiparasitarios')
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
        return super(AntiparasitarioUpdateView, self).form_valid(form)


class AntiparasitarioDeleteView(DeleteView):
    """Empresa Delete View."""

    model = Antiparasitario
    success_url = reverse_lazy('configuracion:antiparasitario_admin')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Empresa Delete View dispatch."""
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(AntiparasitarioDeleteView,
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
