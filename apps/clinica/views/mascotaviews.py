from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import SecurityKey, log_params, UserToken, get_dep_objects
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.db.models import Q

import datetime
import json
from django.contrib.sites.models import Site
from django.core.mail import send_mail

from django.template.loader import render_to_string

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from ..forms.mascotaform import MascotaForm, MascotaUpdateForm

from ..models.mascota import Mascota
from ..models.historia import Historial
from ..models.cliente import Cliente
from ..models.colamedica import ColaMedica
from ..models.atenciones import Atenciones


import logging
log = logging.getLogger(__name__)


# Create your views here.
class MascotaListView(ListView):
    u"""Mascota List"""
    model = Mascota
    paginate_by = settings.PER_PAGE
    template_name = "clinica/index.html"

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(MascotaListView,
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

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(MascotaListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['id_cliente'] = self.kwargs.get('cliente_pk')
        context['listar_mascota'] = Mascota.objects.filter(duenho = self.kwargs.get('cliente_pk'))
        #context['cmi'] = 'mascota' #  Validacion de manual del menu
        context['title'] = ('Seleccione %s'
                            ) % capfirst(' una mascota')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class MascotaCreateView(CreateView):
    """Tipo Documento Identidad."""
    model = Mascota
    form_class = MascotaForm
    template_name = "clinica/form/mascota.html"

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(MascotaCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        """
        context = super(MascotaCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        #context['cmi'] = 'mascota'
        context['title'] = ('Agregar %s') % ('mascota')
        context['subtitle'] = ('Registro %s') % (' de nueva mascota')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.duenho_id = self.kwargs.get('cliente_pk')
        print("=========llega================="),
        self.object.save()

        cantidad= Historial.objects.all()
        historia = Historial(
            num_historia =cantidad.count()+1,
            veterinario = self.request.user,
            mascota = self.object,
            caracter = form.cleaned_data['caracter'],
            actividad = form.cleaned_data['actividad'],
            habitar = form.cleaned_data['habitar'],
            alimentacion = form.cleaned_data['alimentacion'],
            aptitup = form.cleaned_data['aptitup'],
            convive = form.cleaned_data['convive']
        )
        historia.save()

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(MascotaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:mascota_list', kwargs={'cliente_pk':self.object.duenho_id})


class MascotaPerfilView(UpdateView):
    u"""Mascota Perfil """
    model = Mascota
    form_class = MascotaUpdateForm
    template_name = "clinica/mascota/perfil.html"

    def dispatch(self, request, *args, **kwargs):
        return super(MascotaPerfilView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        u"""get_context_data."""
        context = super(MascotaPerfilView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        mascota_pk = self.kwargs.get('pk')
        mascota =  Mascota.objects.get(id=mascota_pk)
        context['mascota_id']  = mascota_pk
        context['mascota'] = Mascota.objects.filter(id=mascota_pk)

        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Atenciones')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        print("=========================")
        msg = ('%(name)s "%(obj)s" fue cambiado satisfacoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(MascotaPerfilView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:mascota_perfil_list', kwargs={'pk': self.object.id})

class MascotaHistoriaListView(ListView):
    u"""Tipo Documento Identidad"""
    model = Atenciones
    paginate_by = settings.PER_PAGE
    template_name = "clinica/mascota/historia.html"

    def dispatch(self, request, *args, **kwargs):
        return super(MascotaHistoriaListView, self).dispatch(request, *args, **kwargs)

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
        context = super(MascotaHistoriaListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['id_cola_medica'] = self.kwargs.get('colamedica_pk')
        context['id_mascota'] = self.kwargs.get('mascota_pk')
        context['historial'] = Atenciones.objects.filter(colamedica__mascota=self.kwargs.get('mascota_pk')).order_by('-created_ath')
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Atenciones')
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class MascotaUpdateView(UpdateView):
    model = Mascota
    form_class = MascotaUpdateForm
    template_name = "clinica/form/mascota.html"

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        return super(MascotaUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MascotaUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Actualizar %s') % ('Mascota')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user

        msg = ('%(name)s "%(obj)s" fue cambiado satisfacoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(MascotaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:mascota_list', kwargs={'cliente_pk': self.object.duenho_id})


class MascotaUpdateActiveView(ListView):
    """ """
    model = Mascota
    template_name = "clinica/mascota.html"

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        state = self.kwargs['state']
        pk = SecurityKey.is_valid_key(request, key, 'mascota_%s' % state)
        if not pk:
            return HttpResponseRedirect(self.get_success_url())
        try:
            self.object = self.model.objects.get(pk=pk)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.get_success_url())

        msg = _('La %(name)s "%(obj)s" %(action)s.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('esta vivo') if state == 'rea' else _('fallecio'))
        }
        mse = _('The %(name)s "%(obj)s" is already %(action)s.') % {
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
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('clinica:mascota_list', kwargs={'cliente_pk': self.object.duenho_id})
