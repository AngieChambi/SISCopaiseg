from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from django.views import generic
from django.db import transaction

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
from ..forms.historiaform import MascotaHistoriDetailForm, HistoriaMascotaForm
from ..models.historia import Historial
from ..models.mascota import Mascota
from apps.clinica.models.cliente import Cliente

import logging
log = logging.getLogger(__name__)

class HistoriasListView(ListView):
    u"""Historias Clinicas"""
    model = Historial
    paginate_by = settings.PER_PAGE
    template_name = "clinica/historia.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(HistoriasListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'num_historia')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.
        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(HistoriasListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Seleccione %s para mas detalle'
                            ) % capfirst(' una historia')
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

class HistoriaFichaListView(ListView):
    u"""Historias Clinicas"""
    model = Historial
    paginate_by = settings.PER_PAGE
    template_name = "clinica/historial/ficha_clinica.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(HistoriaFichaListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'num_historia')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        """"""
        context = super(HistoriaFichaListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['ficha_clinica'] = Historial.objects.filter(mascota = self.kwargs.get("mascota_pk"))
        context['title'] = ('Seleccione %s para mas detalle'
                            ) % capfirst(' una historia')
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

class HistoriaMascotaCreateView(CreateView):
    """  """
    model = Historial
    form_class = HistoriaMascotaForm
    template_name = "clinica/form/historia.html"

    @method_decorator(permission_resource_required(template_name='main/dashboard.html'))
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(HistoriaMascotaCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        """
        context = super(HistoriaMascotaCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        #context['cmi'] = 'mascota'
        context['datos']= Historial.objects.all()
        context['cantidad']=context['datos'].count()+1
        context['title'] = ('Agregar %s') % ('mascota')
        context['subtitle'] = ('Registro %s') % (' de nueva mascota')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        self.object.veterinario = self.request.user
        self.object.mascota_id = self.kwargs.get('mascota_pk')
        self.object.duenho_id = self.kwargs.get('cliente_pk')
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(HistoriaMascotaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:mascota_list', kwargs={'cliente_pk': self.object.duenho_id})

class HistoriaMascotaDetailView(generic.DetailView):
    model = Historial
    success_url = reverse_lazy('clinica:listar_historia')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HistoriaMascotaDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HistoriaMascotaDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'historia'
        context['title'] = _('Detail %s') % capfirst(_('historia'))

        #context['object'] = self.object

        if self.object.mascota:
            initial = {
                'num_historia': self.object.num_historia,
                'created_ath': self.object.created_ath,
                'veterinario': self.object.veterinario,
                'nombre': self.object.mascota.nombre,
                'duenho': self.object.mascota.duenho.persona,
                'direccion': self.object.mascota.duenho.direccion,
                'ciudad': self.object.mascota.duenho.ciudad,
                'telefono': self.object.mascota.duenho.telefono,
                'edad': self.object.mascota.fecha_nacimiento,
                'genero': self.object.mascota.genero,
                'especie': self.object.mascota.especie,
                'raza': self.object.mascota.raza,
                'color': self.object.mascota.color,
            }
        else:
            initial = {
                'username': self.object.username,
                'email': self.object.email,
                'is_superuser': self.object.is_superuser,
                'is_staff': self.object.is_staff,
                'is_active': self.object.is_active,
                'photo': '-',
                'first_name': '-',
                'last_name': '-',
                'identity_type': '-',
                'identity_num': '-',
                'hgroups': UserHeadquar.objects.filter(user=self.object).order_by('headquar'),
                'egroups': UserEnterprise.objects.filter(user=self.object).order_by('enterprise'),
                'agroups': UserAssociation.objects.filter(user=self.object).order_by('association'),
                'status': UserStatus.objects.filter(user=self.object).order_by('-created_at'),
            }
        context['form'] = MascotaHistoriDetailForm(initial=initial)
        return context
