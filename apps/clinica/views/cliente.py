u"""Módulo View Cliente."""
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

from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from apps.params.models import Person

from ..models.cliente import Cliente
from ..forms.cliente import ClienteForm


log = logging.getLogger(__name__)


def PostClienteAjax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            persona = Person()
            persona.first_name = request.POST.get('nombre')
            if request.GET.get('apellidos'):
                persona.last_name = request.POST.get('apellidos')
            else:
                persona.last_name = ""
            if request.GET.get('fecha_de_nacimiento'):
                persona.birth_date = request.POST.get('fecha_de_nacimiento')
            if request.GET.get('tipo_doc'):
                print(request.GET.get('tipo_doc'))
                persona.identity_type = request.POST.get('tipo_doc')
            if request.GET.get('numero'):
                print(request.GET.get('numero'))
                persona.identity_num = request.POST.get('numero')
            persona.save()
            d = Cliente()
            d.persona = Person.objects.last()
            if request.GET.get('direccion'):
                d.direccion = request.POST.get('direccion')
            if request.GET.get('ciudad'):
                d.ciudad = request.POST.get('ciudad')
            if request.GET.get('email'):
                d.email = request.POST.get('email')
            if request.GET.get('telefono'):
                d.telefono = request.POST.get('telefono')
            d.save()
            obj = Cliente.objects.last()
            unidad_json = {}
            unidad_json['pk'] = obj.id
            unidad_json['name'] = obj.persona.first_name
            data_json = json.dumps(unidad_json)
            # else:
            #     data_json = '{"error":"true"}'

        except Exception as e:
            data_json = '{"error":true,"detail":"%s"}' % e
    else:
        data_json = '{"error":"true"}'
    return HttpResponse(data_json, content_type='application/json')


class ClienteListView(ListView):
    u"""Tipo Documento Identidad."""
    model = Cliente
    paginate_by = settings.PER_PAGE
    template_name = "clinica/cliente/index.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ClienteListView,
                     self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        """Paginate."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        """Tipo Doc List Queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'persona__first_name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        """
        """
        context = super(ClienteListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Seleccione %s para editar'
                            ) % capfirst('Cliente')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class ClienteCreateView(CreateView):
    u"""Tipo Documento Identidad."""

    model = Cliente
    form_class = ClienteForm
    template_name = "clinica/cliente/form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(ClienteCreateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        """
        context = super(ClienteCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'tipodoc'
        context['title'] = ('Agregar %s') % ('Cliente')
        return context

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        if form.is_valid():
            persona = Person()
            # print(form.cleaned_data.get("numero"))
            persona.first_name = self.request.POST.get("nombre")
            persona.last_name = self.request.POST.get("apellidos")
            if len(self.request.POST.get("fecha_de_nacimiento")) > 0:
                persona.birth_date = self.request.POST.get(
                    "fecha_de_nacimiento")
            persona.photo = self.request.POST.get("apellido")
            persona.identity_num = self.request.POST.get("numero")
            persona.identity_type = self.request.POST.get("tipo_documento")
            persona.save()
            self.object.persona = persona
            self.object.save()

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(ClienteCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:mascota_list', kwargs={'cliente_pk': self.object.id})


class ClienteUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = Cliente
    form_class = ClienteForm
    template_name = "clinica/cliente/form.html"
    success_url = reverse_lazy("clinica:cliente_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """Tipo Documento Create View dispatch."""

        return super(ClienteUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(ClienteUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Actualizar %s') % ('Cliente')
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
        return super(ClienteUpdateView, self).form_valid(form)

    def get_initial(self):
        context = super(ClienteUpdateView, self).get_initial()
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


class ClienteDeleteView(DeleteView):
    """Empresa Delete View."""

    model = Cliente
    success_url = reverse_lazy('clinica:cliente_list')

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
        return super(ClienteDeleteView,
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
