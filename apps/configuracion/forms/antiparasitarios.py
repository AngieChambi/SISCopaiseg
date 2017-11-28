u"""Módulo Especie Form."""

from django import forms
from ..models.antiparasitarios import Antiparasitario
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from crispy_forms.helper import FormHelper, Layout
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list


class AntiparasitarioForm(forms.ModelForm):
    u"""Especie Form."""
    especie= forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': 'hidden'}))
    class Meta:
        """Meta."""
        model = Antiparasitario
        fields = ('nombre',)
        exclude=('especie',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(AntiparasitarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(Field('especie', placeholder='Ingrese nombre del antiparasitario',
                      css_class='input-required especie')),
            Div(Field('nombre', placeholder='Ingrese nombre del antiparasitario',
                      css_class='input-required col-md-1')),
            FormActions(
                smtSave(),
            ),
        )
