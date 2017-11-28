u"""Módulo Vacuna Form."""
from django import forms
from apps.params.models import IDENTITY_TYPE_CHOICES
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from crispy_forms.helper import FormHelper, Layout
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list

from ..models.vacunacion import Vacunacion

class VacunacionForm(forms.ModelForm):
    u"""Vacuna Form."""

    class Meta:
        """Meta."""
        model = Vacunacion
        exclude = ('atenciones',)
        fields = ('motivo','vacuna','observacion',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(VacunacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div(Field('motivo', placeholder='Ingrese el motivo de vacunación'),
                    css_class='col-md-12'),
                Div(Field('vacuna',),
                    css_class='col-md-12'),
                Div(Field('observacion', placeholder='Ingrese un la nota'),
                    css_class='col-md-12'),
            ),

            Div(Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),),
        )
