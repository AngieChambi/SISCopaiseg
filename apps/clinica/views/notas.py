from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from django.views import generic
from django.db import transaction

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
from ..forms.notas import NotasForm
import os
from ..models.nota import Notas
from ..models.atenciones import Atenciones, ArchivosAdjuntos


import logging
log = logging.getLogger(__name__)


class NotasCreateView(CreateView):
    """  """
    model = Notas
    form_class = NotasForm
    template_name = "clinica/atenciones/notas_form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotasCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotasCreateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'consulta'
        context['title'] = _('Add %s') % capfirst(_('consulta'))
        context['mas'] = self.kwargs.get('colamedica_pk')
        context['colamedica_id'] = self.kwargs.get('colamedica_pk')
        context['subtitle'] = _('Registro de %s') % capfirst(_('Consulta'))
        return context

    def get_form_kwargs(self):
        kwargs = super(NotasCreateView, self).get_form_kwargs()
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
        return super(NotasCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clinica:historia_list', kwargs={'mascota_pk': self.kwargs.get("mascota_pk"), 'colamedica_pk': self.kwargs.get("colamedica_pk")})


@require_POST
def upload( request ):
    file = upload_receive( request )

    #para doctores multiples se tiene que cambiar la consulta de atenciones
    instance = ArchivosAdjuntos( file = file, atenciones = Atenciones.objects.last())
    instance.save()

    basename = os.path.basename( instance.file.path )

    file_dict = {
        'name' : basename,
        'size' : file.size,

        'url': settings.MEDIA_URL + basename,
        'thumbnailUrl': settings.MEDIA_URL + basename,

        'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )

@require_POST
def upload_delete( request, pk ):
    success = True
    try:
        instance = ArchivosAdjuntos.objects.get( pk = pk )
        os.unlink( instance.file.path )
        instance.delete()
    except ArchivosAdjuntos.DoesNotExist:
        success = False

    return JFUResponse( request, success )
