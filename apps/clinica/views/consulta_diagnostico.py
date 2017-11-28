from backengo.utils.decorators import permission_resource_required
from backengo.utils.forms import empty
from backengo.utils.security import get_dep_objects, log_params, SecurityKey

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from ..models.consulta import Diagnostico

import logging
log = logging.getLogger(__name__)

from django.core import serializers

import json

def get_diagnosticos(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        results =[]
        drugs = Diagnostico.objects.filter(nombre__contains = q )[:20]
        print("Imprimeido los drugs",drugs)
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id
            drug_json['label'] = drug.nombre
            drug_json['value'] = drug.nombre
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'No se puede obtener datos'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
