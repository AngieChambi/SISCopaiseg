u"""Módulo View Tipo Documento."""

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
import json
from ..models.acopio import Acopio
from ..forms.acopio import AcopioForm
from ..models.detalle_acopio import DetalleAcopio
from apps.ventas.models.Producto import Producto
from django.db import transaction
import logging
from decimal import Decimal
log = logging.getLogger(__name__)


class AcopioListView(ListView):
    u"""Tipo Documento Identidad."""

    model = Acopio
    paginate_by = settings.PER_PAGE
    template_name = "acopios/acopio/index.html"

    # @method_decorator(Acopioon_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(AcopioListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'socio__cod_socio')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(AcopioListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Acopio')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class AcopioCreateView(CreateView):
    u"""Tipo Documento Identidad."""
    model = Acopio
    form_class = AcopioForm
    template_name = "acopios/acopio/form.html"
    # success_url = reverse_lazy("acopios:acopio_add")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(AcopioCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Tipo Documento Identidad ListView List get context.

        Funcion con los primeros datos iniciales para la carga del template.
        """
        context = super(AcopioCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'tipodoc'
        context['title'] = 'Nuevo Acopio'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            acopio = json.loads(self.request.POST.get('data_acopio'))
            print(acopio)
            self.object.total = acopio['total']
            print("asdkashkjdhksajhdkjahskjh")
            self.object.usuario = self.request.user
            self.object.save()
            for p in acopio['productos']:
                productos = Producto.objects.get(pk=p["id"])

                productos.existencia = productos.existencia + \
                    (int(p['cantidad']) *
                     (productos.unidad_medida.cant_equivalencia))
                productos.MontoReal = productos.precioV * productos.existencia
                productos.igv = productos.MontoReal * Decimal(0.18)

                productos.save()
                dv = DetalleAcopio(
                    producto_id=p['id'],
                    acopio=self.object,
                    kilos=p['cantidad'],
                    total_pagar=p['importe']
                )
                dv.save()
        except Exception as e:
            print(e)
            messages.error(self.request, e)

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }

        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(AcopioCreateView, self).form_valid(form)


class AcopioUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Acopio
    form_class = AcopioForm
    template_name = "acopios/acopio/form.html"
    success_url = reverse_lazy("acopios:acopio_list")

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

        return super(AcopioUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(AcopioUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Actualizar %s') % ('Acopio')
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
        return super(AcopioUpdateView, self).form_valid(form)
