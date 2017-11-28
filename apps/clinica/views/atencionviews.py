from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from django.views import generic
from django.db import transaction

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from ..forms.atencionform import AtencionForm, AtencionMascotaDetailForm
from ..models.atencion import Atencion
from apps.ventas.models.Producto import Producto

from ..models.atenciones import Atenciones
from ..forms.atenciones import AtencionesForm
from ..models.colamedica import ColaMedica
from ..models.mascota import Mascota
import logging
log = logging.getLogger(__name__)

class AtencionHistoriaListView(ListView):
    u"""Tipo Documento Identidad"""
    model = Atenciones
    paginate_by = settings.PER_PAGE
    template_name = "clinica/historial/historia.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AtencionHistoriaListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        u"""get_paginate_by."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        u"""get_queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'created_ath')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        u"""get_context_data."""
        context = super(AtencionHistoriaListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['id_cola_medica'] = self.kwargs.get('colamedica_pk')
        print("cola medica", self.kwargs.get('colamedica_pk'))
        context['id_mascota'] = self.kwargs.get('mascota_pk')
        context['historial'] = Atenciones.objects.filter(colamedica__mascota=self.kwargs.get('mascota_pk')).order_by('-created_ath')
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Atenciones')
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

class AtencionListView(ListView):
    u"""Tipo Documento Identidad"""
    model = Atenciones
    paginate_by = settings.PER_PAGE
    template_name = "clinica/historial/index.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AtencionListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        u"""get_paginate_by."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        u"""get_queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'created_ath')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        u"""get_context_data."""
        context = super(AtencionListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['id_cola_medica'] = self.kwargs.get('colamedica_pk')
        print("colamedica_pk", self.kwargs.get('colamedica_pk'))
        context['id_mascota'] = self.kwargs.get('mascota_pk')
        context['mascota'] = Mascota.objects.filter(id=18)
        context['historial'] = Atenciones.objects.filter(colamedica__mascota=self.kwargs.get('mascota_pk'))
        mascotas = Mascota.objects.get( id = self.kwargs.get('mascota_pk'))
        print("sssssssssssssssssssssssssssssssssssssss",mascotas)
        context['mascota_nombre'] = mascotas.nombre
        context['mascota_raza'] = mascotas.raza
        context['mascota_genero'] = mascotas.genero
        context['mascota_dueño'] = mascotas.duenho

        vacuna = Producto.objects.filter(state=True)

        context['vacunas'] =vacuna

        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Atenciones')
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class AtencionCreateView(CreateView):
    """  """
    model = Atenciones
    form_class = AtencionesForm
    template_name = "clinica/historial/index.html"

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(AtencionCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        u"""get_context_data."""
        context = super(AtencionCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['id_cola_medica'] = self.kwargs.get('colamedica_pk')
        context['id_mascota'] = self.kwargs.get('mascota_pk')
        context['id'] = self.kwargs.get('pk')
        context['mascota'] = Mascota.objects.filter(id=18)
        context['historial'] = Atenciones.objects.filter(colamedica__mascota=self.kwargs.get('mascota_pk'))
        mascotas = Mascota.objects.get( id = self.kwargs.get('mascota_pk'))
        print("sssssssssssssssssssssssssssssssssssssss",mascotas)
        context['mascota_nombre'] = mascotas.nombre
        context['mascota_raza'] = mascotas.raza
        context['mascota_genero'] = mascotas.genero
        context['mascota_dueño'] = mascotas.duenho
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Atenciones')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        try:
            print("hola")
            self.object = form.save(commit=False)
            self.object.veterinario = self.request.user
            self.object.colamedica_id = self.kwargs.get('colamedica_pk')
            print("========funciona=========")
            msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }

            if self.object.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
            return super(AtencionCreateView, self).form_valid(form)

        except Exception as e:
            msg = _('La %(name)s  para la mascota %(obj)s ya existe')% {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }
            messages.warning(self.request, msg)
            log.warning(force_text(msg), extra=log_params(self.request))
            return super(AtencionCreateView, self).form_invalid(form)


    def get_success_url(self):
        return reverse('clinica:historia_list', kwargs={'mascota_pk': self.kwargs.get('mascota_pk'),'colamedica_pk':self.object.colamedica_id})


class AtencionTerminadaView(ListView):
    """ """
    model = ColaMedica
    template_name = "clinica/colamedica.html"
    success_url = reverse_lazy("clinica:listar_medica")

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        state = self.kwargs['state']
        pk = SecurityKey.is_valid_key(request, key, 'colamedica_%s' % state)
        if not pk:
            return HttpResponseRedirect(self.success_url)
        try:
            self.object = self.model.objects.get(pk=pk)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        msg = _('La %(name)s del paciente "%(obj)s" %(action)s satisfactoriamente.') % {
            'name': capfirst(force_text('atencion medica')),
            'obj': force_text(self.object),
            'action': (_('reactivated') if state == 'rea' else _('Terminó'))
        }
        mse = _('La %(name)s "%(obj)s" is already %(action)s.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('active') if state == 'rea' else _('inactive'))
        }
        try:
            if state == 'ina' and not self.object.is_active:
                raise Exception(mse)
            else:
                if state == 'rea' and self.object.is_active:
                    raise Exception(mse)
                else:
                    self.object.is_active = (True if state == 'rea' else False)
                    self.object.save()
                    messages.success(self.request, msg)
                    log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.warning(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)
