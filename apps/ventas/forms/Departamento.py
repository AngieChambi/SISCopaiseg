from django import forms
from ..models.Departamento import Departamento
from backengo.utils.forms import smtSave, btnCancel, btnReset
from crispy_forms.helper import FormHelper, Layout
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, StrictButton, FieldWithButtons
from crispy_forms.helper import FormHelper, Layout


class DepartamentoForm(forms.ModelForm):
    u"""Tipo Documeto Form."""

    class Meta:
        """Meta."""

        model = Departamento
        exclude = ()
        Field = ('descripcion')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Div(Field('descripcion', css_class='col-md-3')),
                    ),
                    css_class='modal-body'
                ),
                Div(Row(
                    FormActions(
                        smtSave(),
                        btnCancel(),
                        btnReset(),
                    ),
                ), css_class='modal-footer',),
            ),
        )
