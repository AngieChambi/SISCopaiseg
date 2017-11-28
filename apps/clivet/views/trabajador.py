u"""Módulo View Cliente."""

from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey
from apps.params.models import Person
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

from apps.sad.models import User
from ..forms.trabajador import TrabajadorForm
from apps.sad.models import User
from apps.sad.forms import UserForm
from apps.params.models import Person
from django.contrib.auth.models import Permission, Group
from apps.space.models import Solution, Headquar
from backengo.utils.security import SecurityKey, log_params, UserToken, get_dep_objects
from django.db import transaction
from apps.sad.models import Module, Menu, User, UserAssociation, UserEnterprise, \
    UserHeadquar, BACKEND, UserStatus, Ticket
import json
import logging
log = logging.getLogger(__name__)


class TrabajadorUpdateView(UpdateView):
    """Tipo Documento Update View."""

    model = User
    form_class = TrabajadorForm
    template_name = "clivet/trabajador/form.html"
    success_url = reverse_lazy("clivet:clivet")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk:
            self.kwargs['pk'] = request.user.pk
        else:
            return HttpResponseRedirect(self.success_url)

        return super(TrabajadorUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Tipo Documento Update View context data."""
        context = super(TrabajadorUpdateView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        # context['cmi'] = 'empresa'
        context['title'] = ('Editar %s') % ('Perfil')
        return context

    def form_valid(self, form):
        """Tipo Documento Update View form_valid."""
        self.object = form.save(commit=False)
        if form.is_valid():
            if self.object.person:
                self.object.person.first_name = self.request.POST.get(
                    "nombre")
                self.object.person.last_name = self.request.POST.get(
                    "apellidos")
                self.object.person.birth_date = self.request.POST.get(
                    "fecha_de_nacimiento")
                self.object.person.identity_num = self.request.POST.get(
                    "numero")
                self.object.person.identity_type = self.request.POST.get(
                    "tipo_documento")
                self.object.person.photo = self.request.POST.get(
                    "photo")
                self.object.person.save()
            else:
                person = Person()
                person.first_name = self.request.POST.get("nombre")
                person.last_name = self.request.POST.get("apellidos")
                person.birth_date = self.request.POST.get(
                    "fecha_de_nacimiento")
                person.identity_num = self.request.POST.get("numero")
                person.identity_type = self.request.POST.get("tipo_documento")
                person.photo = self.request.POST.get("photo")
                person.save()
                self.object.person = person()
            self.object.save()

        msg = ('%(name)s "%(obj)s" fue cambiado satisfacoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(TrabajadorUpdateView, self).form_valid(form)

    def get_initial(self):
        context = super(TrabajadorUpdateView, self).get_initial()
        context = context.copy()
        if self.object.person:
            context['nombre'] = self.object.person.first_name
            context['apellidos'] = self.object.person.last_name
            context['tipo_documento'] = self.object.person.identity_type
            context['numero'] = self.object.person.identity_num
            context['fecha_de_nacimiento'] = self.object.person.birth_date and self.object.person.birth_date.strftime(
                "%Y-%m-%d") or ""
            context['photo'] = self.object.person.photo

        return context
