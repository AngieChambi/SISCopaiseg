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

from ..models.detallecompra import DetalleCompra
from ..models.compra import Compra
import logging
log = logging.getLogger(__name__)


class DetalleCompraListView(ListView):
    u"""Tipo Documento Identidad."""

    model = DetalleCompra
    template_name = "compras/detallecompra/index.html"

    def get_context_data(self, **kwargs):
        #mascota = Mascota.objects.get(nombre='Boby')
        context = super(DetalleCompraListView, self).get_context_data(**kwargs)
        context['lista'] = DetalleCompra.objects.filter(
            compra_id=self.kwargs['id'])
        context['opts'] = self.model._meta
        # context['cmi'] = 'menu' #  Validacion de manual del menu
        context['title'] = ('Detalle de compra')
        context['compras'] = (Compra.objects.get(id=self.kwargs['id']))
        return context
        return context
