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
from django.core.serializers.json import DjangoJSONEncoder


from ..models.mascota import Mascota
from ..models.cliente import Cliente

from ..models.consulta import Diagnostico
from ..models.historia import Historial
from ..models.colamedica import ColaMedica
from ..forms.colamedicaform import ColaMedicaForm
from apps.ventas.models.Producto import Producto
import logging
log = logging.getLogger(__name__)


import json


def BuscarProducto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        results = []
        productos = Producto.objects.filter(
            nombre__contains=q)[:5]
        for producto in productos:
            producto_json = {}
            producto_json['id'] = producto.id
            producto_json['label'] = producto.nombre
            producto_json['value'] = producto.nombre
            producto_json['nombre'] = producto.nombre
            producto_json['precioV'] = producto.precioV
            producto_json['precioC'] = producto.precioC
            producto_json['existencia'] = producto.existencia
            producto_json['igv'] = producto.igv
            results.append(producto_json)
        data = json.dumps(results, cls=DjangoJSONEncoder)
    else:
        data = 'No se puede obtener datos'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_drugs(request):
    if request.is_ajax():
        q = request.GET.get('term', '')

        results =[]
        drugs = Mascota.objects.filter(duenho__persona__first_name__contains = q )[:20]
        print("IMprimeido los drugs",drugs)
        if  drugs:
            print("holaaaaaaaaaaaaaaaaaaa")
            drugs = Mascota.objects.filter(duenho__persona__first_name__contains = q )[:20]

            results = []
            for drug in drugs:
                drug_json = {}
                drug_json['id'] = drug.id
                drug_json['nombre_mascota'] = drug.nombre
                drug_json['label'] = drug.duenho.persona.first_name + ' ' + drug.nombre
                drug_json['value'] = drug.duenho.persona.first_name
                drug_json['cliente_id'] = drug.duenho.id

                #drug_json['pk'] = serializers.serialize('json', drug.mascotas.all(), fields=('id','nombre'))
                #drug_json['mascota_atencion'] = drug.nombre
                results.append(drug_json)
                print(results)
        if not drugs:
            print("fgggggggggggggggggggg")
            drugs = Cliente.objects.filter(
                persona__first_name__contains=q)[:20]
            results = []
            for drug in drugs:
                drug_json = {}
                drug_json['cliente_id'] = drug.id
                drug_json['label'] = drug.persona.first_name
                drug_json['value'] = drug.persona.first_name
                #drug_json['pk'] = serializers.serialize('json', drug.mascotas.all(), fields=('id','nombre'))
                #drug_json['mascota_atencion'] = drug.nombre
                results.append(drug_json)
                print(results)
        data = json.dumps(results)
    else:
        data = 'No se puede obtener datos'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
