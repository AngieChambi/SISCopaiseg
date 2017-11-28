from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from django.views import generic
from django.db import transaction

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

from ..forms.vacunacion import VacunacionForm

from ..models.vacunacion import Vacunacion
from ..models.atenciones import Atenciones
import json
import logging
log = logging.getLogger(__name__)


class VacunacionCreateView(CreateView):
    """  """
    model = Vacunacion
    form_class = VacunacionForm
    template_name = "clinica/atenciones/vacuna_form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(VacunacionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VacunacionCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'consulta'
        context['title'] = _('Add %s') % capfirst(_('consulta'))
        context['mas'] = self.kwargs.get('colamedica_pk')
        context['colamedica_id'] = self.kwargs.get('colamedica_pk')
        context['subtitle'] = _('Registro de %s') % capfirst(_('Consulta'))
        return context

    def get_form_kwargs(self):
        kwargs = super(VacunacionCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """"Empresa Crete View  form valid."""
        self.object = form.save(commit=False)
        self.object.veterinario = self.request.user
        atenciones = Atenciones.objects.filter(colamedica_id=self.kwargs.get('colamedica_pk')).latest('id')
        self.object.atenciones = atenciones
        print("===========//==============")
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(VacunacionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:historia_list', kwargs={'mascota_pk': self.kwargs.get("mascota_pk"), 'colamedica_pk': self.kwargs.get("colamedica_pk")})


def PostVacunacionAjax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = Vacunacion()
            d.atenciones = Atenciones.objects.last()
            d.motivo = request.POST.get('motivo')
            d.vacuna_id = request.POST.get('vacuna')
            d.dosis = request.POST.get('dosis')
            d.observacion = request.POST.get('observacion')
            print("se fuardo")
            d.save()

            obj = Vacunacion.objects.last()
            unidad_json = {}
            unidad_json['pk'] = obj.id
            unidad_json['vacuna'] = '%s' % (obj.vacuna)
            data_json = json.dumps(unidad_json)
        except Exception as e:
            data_json = '{"data":"fail"}'
            print(e)
    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')
