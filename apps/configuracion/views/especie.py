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

from ..models.especie import Raza, Especie, Color
from ..forms.especie import RazaForm

log = logging.getLogger(__name__)


import json
from django.core import serializers

class EspecieAdministrarView(TemplateView):
    u"""Tipo Documento Identidad."""
    model = Raza
    template_name = "configuracion/especie/index.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(EspecieAdministrarView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        """
        context = super(EspecieAdministrarView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta

        context['title'] = ('Agregar %s') % ('especie')
        return context


class EspecieListView(ListView):
    u"""Tipo Documento Identidad."""
    model = Especie
    template_name = "configuracion/especie/list_especie.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(EspecieListView,
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
        """
        context = super(EspecieListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        especies =   Especie.objects.all()


        cantidad = Especie.objects.all().count()


        context["especies"]=especies

        if cantidad == 1:
            print("True")
        if  cantidad == 2:
            context['uno'] = '6'
            print("False")
        if  cantidad == 3:
            context['uno'] = '4'
            print("FalseTrue")
        if  cantidad == 4:
            context['uno'] = '3'
        else:
            context['uno'] = '3'
            print("FalseTrue")
        context['title'] = ('Seleccione %s para editar'
                            ) % capfirst('especie')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context

class RazaListView(ListView):
    u"""Tipo Documento Identidad."""
    model = Raza
    template_name = "configuracion/especie/list_raza.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(RazaListView,
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
        """
        context = super(RazaListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['especie_raza'] = Raza.objects.filter(especie=self.kwargs.get('especie_pk'))

        context['id_form']=self.kwargs.get('especie_pk')
        context['id_especie']=self.kwargs.get('especie_pk')
        print("id_especie:",self.kwargs.get('especie_pk'))
        context['title'] = ('Seleccione %s para editar'
                            ) % capfirst('especie')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context

class ColorListView(ListView):
    u"""Tipo Documento Identidad."""
    model = Color
    template_name = "configuracion/especie/list_color.html"


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ColorListView,
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
        """
        context = super(ColorListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['raza_color'] = Color.objects.filter(raza=self.kwargs.get('raza_pk'))
        context['id_form']=self.kwargs.get('raza_pk')
        context['id_especie']=self.kwargs.get('especie_pk')
        context['title'] = ('Seleccione %s para editar'
                            ) % capfirst('especie')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


def PostEspecieAjax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = Especie()
            d.nombre = request.POST.get('nombre')
            print("se guardo")
            d.save()

            obj = Especie.objects.last()
            unidad_json = {}
            unidad_json['pk'] = obj.id
            unidad_json['nombre'] = '%s' % (obj.nombre)
            data_json = json.dumps(unidad_json)
            print("jjjjjjjjjjjjjjjj")
        except Exception as e:
            data_json = '{"data":"fail"}'
            print(e)
    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')


def PostRazaAjax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = Raza()
            d.especie_id = request.POST.get('id')
            d.nombre = request.POST.get('nombre')
            print("se fuardo")
            d.save()

            obj = Raza.objects.last()
            unidad_json = {}
            unidad_json['pk'] = obj.id
            unidad_json['nombre'] = '%s' % (obj.nombre)
            data_json = json.dumps(unidad_json)
            print("jjjjjjjjjjjjjjjj")
        except Exception as e:
            data_json = '{"data":"fail"}'
            print(e)
    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')


def PostColorAjax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = Color()
            d.especie_id = request.POST.get('id_especie')
            d.raza_id = request.POST.get('id')
            d.nombre = request.POST.get('nombre')
            print("se guardo el color")
            d.save()

            obj = Color.objects.last()
            unidad_json = {}
            unidad_json['pk'] = obj.id
            unidad_json['nombre'] = '%s' % (obj.nombre)
            data_json = json.dumps(unidad_json)
            print("jjjjjjjjjjjjjjjj")
        except Exception as e:
            data_json = '{"data":"fail"}'
            print(e)
    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')

def PostVacunacionAjax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = Especie()
            d.nombre = request.POST.get('nombre')
            print("se fuardo")
            d.save()

            obj = Especie.objects.last()
            unidad_json = {}
            unidad_json['pk'] = obj.id
            unidad_json['nombre'] = '%s' % (obj.nombre)
            data_json = json.dumps(unidad_json)
        except Exception as e:
            data_json = '{"data":"fail"}'
            print(e)
    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')

class EspecieUpdateView(UpdateView):
    """Especie View"""

    model = Especie
    form_class = RazaForm
    template_name = "configuracion/especie/form.html"
    success_url = reverse_lazy("configuracion:especie_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Tipo Documento Create View dispatch."""

        return super(EspecieUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(EspecieUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Actualizar %s') % ('especie')
        return context

    def form_valid(self, form):
        """Tipo Documento Update View form_valid."""
        self.object = form.save(commit=False)
        if form.is_valid():
            if self.object.persona:
                self.object.persona.first_name = self.request.POST.get(
                    "nombre")
                self.object.persona.last_name = self.request.POST.get(
                    "apellidos")
                if len(self.request.POST.get("fecha_de_nacimiento")) > 0:
                    self.object.persona.birth_date = self.request.POST.get(
                        "fecha_de_nacimiento")
                self.object.persona.identity_num = self.request.POST.get(
                    "numero")
                self.object.persona.identity_type = self.request.POST.get(
                    "tipo_documento")
                self.object.persona.photo = self.request.POST.get(
                    "foto_perfil")
                self.object.persona.save()
                self.object.save()

        msg = ('%(name)s "%(obj)s" fue cambiado satisfacoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(EspecieUpdateView, self).form_valid(form)

    def get_initial(self):
        context = super(EspecieUpdateView, self).get_initial()
        context = context.copy()
        if self.object.persona:
            context['nombre'] = self.object.persona.first_name
            context['apellidos'] = self.object.persona.last_name
            context['tipo_documento'] = self.object.persona.identity_type
            context['numero'] = self.object.persona.identity_num
            context['fecha_de_nacimiento'] = self.object.persona.birth_date and self.object.persona.birth_date.strftime(
                "%Y-%m-%d") or ""
            context['foto_perfil'] = self.object.persona.photo

        return context


class EspecieDeleteView(DeleteView):
    """Empresa Delete View."""

    model = Especie
    success_url = reverse_lazy('configuracion:especie_list')

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
        return super(EspecieDeleteView,
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
