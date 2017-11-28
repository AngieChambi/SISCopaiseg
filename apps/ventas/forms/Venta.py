from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst, get_text_list
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab

from unicodedata import normalize
from backengo.utils.security import UserToken
from django.db.models import Q
from django.core.exceptions import NON_FIELD_ERRORS
from ..models.Venta import Venta
from apps.ventas.models.Producto import Producto
from apps.sad.models import User
from apps.params.models import IDENTITY_TYPE_CHOICES


class VentaForm(forms.ModelForm):
    u"""Tipo Documeto Form."""
    data_venta = forms.CharField(
        required=False,  widget=forms.TextInput(attrs={'type': 'hidden'}))
    producto = forms.CharField(label="", required=False,
                               widget=forms.TextInput(attrs={'type': 'none', 'class': 'form-control busqueda-producto-imput ', 'placeholder': 'Buscar Producto o Servicio', 'autofocus': 'autofocus'}))

    tipo_doc = forms.ChoiceField(
        choices=IDENTITY_TYPE_CHOICES, required=False,
        label='Tipo de documento')

    class Meta:

        model = Venta
        fields = ('total', 'igv',)
        exclude = ('cliente', 'codigo')
        widgets = {
            'total': forms.TextInput(attrs={'class': 'form-control'}),
            'igv': forms.TextInput(attrs={'class': 'form-control'}),
        }
