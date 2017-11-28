from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.shortcuts import render
from backengo.utils.decorators import permission_resource_required
from django.utils.decorators import method_decorator
from django.db.models import *
from datetime import *
from ...ventas.models.Producto import Producto
from ...compras.models.compra import Compra
from ...compras.models.Proveedor import Proveedor
from ...ventas.models.Venta import Venta
from ...clinica.models.cliente import Cliente
from ...clinica.models.colamedica import ColaMedica
from ...clinica.models.atenciones import Atenciones
from ...clinica.models.mascota import Mascota
from ...citas.models.cita import Cita
from django.core.serializers.json import DjangoJSONEncoder

from django.core import serializers
from django.contrib.auth.decorators import login_required
import json


#@login_required(login_url="/accounts/login/")
class MainView(TemplateView):
    template_name = "main/dashboard.html"
    context_object_name = 'dashboard'
    @method_decorator(login_required)
    #@method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        """dispatch."""
        return super(MainView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        a=Venta.objects.filter(fechav__month=datetime.now().month).aggregate(total=Sum('total')).get('total')
        if a==None:
             a=0

        context = super(MainView, self).get_context_data(**kwargs)
        context['venta'] = Venta.objects.all().count()
        context['compra'] = Compra.objects.all().count()
        context['proveedor'] = Proveedor.objects.all().count()
        context['cliente'] = Cliente.objects.all().count()
        context['atencion'] = Atenciones.objects.all().count()
        context['colamedica'] = ColaMedica.objects.all().count()
        context['mascota'] = Mascota.objects.all().count()
        context['cita'] = Cita.objects.filter(date__lte=datetime.now()).count()
        context['bienes']=Producto.objects.all().aggregate(total_soles=Sum(F('existencia')*F('precioV'))).get('total_soles')
        context['monto']=a


        return context

# def clivet(request):
#     c = dict(
#         cmi='d',
#         opts=_('Home'),
#         title=_('Backend Home Page.'),
#     )
#     print("hola")
#     return render(request, 'main/dashboard.html', c)
