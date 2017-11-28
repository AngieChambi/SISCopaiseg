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

from ..forms.atencionform import AtencionForm, ConsultaForm

from ..models.atenciones import Atenciones
from ..models.atencion import Atencion
from ..models.consulta_diagnostico import ConsultaDiagnostico
from ..models.consulta_pruebas_auxiliares import ConsultaPruebasAuxiliares
from ..models.consulta_tratamiento import ConsultaTratamiento
from ..models.consulta import HallasgosClinicos
from ..models.colamedica import Mascota
import json
from django.utils.timezone import timedelta
from django.utils import timezone
import time
import logging
log = logging.getLogger(__name__)


class ConsultaCreateView(CreateView):
    """  """
    model = Atencion
    form_class = ConsultaForm
    template_name = "clinica/atenciones/consulta_form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):

        return super(ConsultaCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConsultaCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'consulta'
        context['datos']= Atencion.objects.all()
        context['cantidad']=context['datos'].count()+1
        context['title'] = _('Add %s') % capfirst(_('consulta'))

        mascota = Mascota.objects.get(colamedica__id = self.kwargs.get('colamedica_pk'))

        context['mascota_nombre'] = mascota.nombre
        context['mascota_raza'] = mascota.raza
        context['mascota_genero'] = mascota.genero
        context['mascota_dueño'] = mascota.duenho

        context['fecha'] =time.strftime("%x")
        context['horta'] = time.strftime("%X")

        context['subtitle'] = _('Registro de %s') % capfirst(_('Consulta'))
        return context

    def get_form_kwargs(self):
        kwargs = super(ConsultaCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        #cual es el control activo que pertenece a su institución
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.atenciones = Atenciones.objects.last()
        self.object.save()
        print("==============================0")
        print(self.request.POST.get("data_diagnostico"))
        print(self.request.POST)
        data = json.loads(self.request.POST.get("data_diagnostico"))
        print("data:", data)
        for p in data['diagnosticos']:
            dv = ConsultaDiagnostico(
                consulta=self.object,
                diagnostico_id=p['id'],
                tipo_diagnostico=p['tipo_diagnostico']
            )
            dv.save()
        print("==========================================")
        for p in data['pruebas_auxiliares']:
            dv = ConsultaPruebasAuxiliares(
                consulta=self.object,
                pruebas_auxiliares_id=p['id'],
                indicacion=p['indicacion']
            )
            dv.save()
        print("==========================================")
        for p in data['tratamientos']:
            dv = ConsultaTratamiento(
                consulta=self.object,
                tratamientos_id=p['id'],
                indicacion=p['indicacion']
            )
            dv.save()
        print("==========================================")

        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(ConsultaCreateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('clinica:historia_list', kwargs={'mascota_pk': self.kwargs.get("mascota_pk"), 'colamedica_pk': self.kwargs.get("colamedica_pk")})


class ConsultaUpdateView(UpdateView):
    """  """
    model = Atencion
    form_class = ConsultaForm
    template_name = "clinica/atenciones/consulta_form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsultaUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConsultaUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'consulta'
        context['datos']= Atencion.objects.all()
        context['cantidad']=context['datos'].count()+1
        context['title'] = _('Add %s') % capfirst(_('consulta'))
        context['colamedica_id'] = self.kwargs.get('colamedica_pk')
        context['subtitle'] = _('Registro de %s') % capfirst(_('Consulta'))
        return context

    def get_form_kwargs(self):
        kwargs = super(ConsultaUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        self.object.veterinario = self.request.user
        self.object.atenciones_id = self.kwargs.get('atencion_pk')

        msg = _(' %(name)s "%(obj)s" fue  actualizado satisfactoriamente') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(ConsultaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:atenciones_add', kwargs={'mascota_pk': self.kwargs.get("mascota_pk"), 'colamedica_pk': self.kwargs.get("colamedica_pk")})

class ConsultaDeleteView(DeleteView):
    model = Atencion

    def dispatch(self, request, *args, **kwargs):
        return super(ConsultaDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.atenciones = Atenciones.objects.get(atencion=self.kwargs['pk'])
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(
                    self.request,
                    ('No se puede eliminar %(name)s)') %
                    {
                        "name":
                            capfirst(force_text(
                                self.model._meta.verbose_name)
                            ) + '"' + force_text(d) + '"'
                    })
                raise Exception(msg)
            d.delete()
            msg = (' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.danger(request, e)
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('clinica:atenciones_add', kwargs={'mascota_pk': self.kwargs.get("mascota_pk"), 'colamedica_pk': self.kwargs.get("colamedica_pk")})
