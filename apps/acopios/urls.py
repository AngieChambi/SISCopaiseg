from django.conf.urls import url
from apps.acopios.views.acopio import AcopioCreateView

urlpatterns = [
    # Proveedor
    url(r'^acopio/crear/$', AcopioCreateView.as_view(), name="acopio_add"),
]
