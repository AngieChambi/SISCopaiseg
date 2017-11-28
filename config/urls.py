"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django import views as django_views

from apps.clinica.views.notas import upload, upload_delete

from apps.clivet.views.main import  MainView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/', django_views.i18n.javascript_catalog),
    # =============================================================
    #                           backengo
    # =============================================================
    url(r'^mod_backend/', include('apps.mod_backend.urls', namespace='mod_backend')),
    url(r'^space/', include('apps.space.urls', namespace='space')),
    url(r'^sad/', include('apps.sad.urls', namespace='sad')),
    url(r'^accounts/', include('apps.accounts.urls')),
    # =============================================================
    #                           clivet
    # =============================================================


    url( r'upload/', upload, name = 'jfu_upload' ),
    url( r'^delete/(?P<pk>\d+)$', upload_delete, name = 'jfu_delete' ),

    # url(r'^about/$', AboutView.as_view()),
    url(r'^$', MainView.as_view(), name='dashboard'),

    url(r'^', include('apps.clivet.urls', namespace='clivet')),
    url(r'^clinica/', include('apps.clinica.urls', namespace='clinica')),
    url(r'^ventas/', include('apps.ventas.urls', namespace='ventas')),
    url(r'^configuracion/', include('apps.configuracion.urls', namespace='configuracion')),
    url(r'^compras/', include('apps.compras.urls', namespace='compras')),
    url(r'^citas/', include('apps.citas.urls', namespace='citas')),
    url(r'^acopios/', include('apps.acopios.urls', namespace='acopios')),
    # TODO: Poner en la aplicacion que se usa
    url(r'^chaining/', include('smart_selects.urls')),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
