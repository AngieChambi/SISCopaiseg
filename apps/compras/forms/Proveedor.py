from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row
from django import forms
from django.utils.text import capfirst

from apps.compras.models.Proveedor import Proveedor
from backengo.utils.forms import smtSave, btnCancel, btnReset


class ProveedorForm(forms.ModelForm):

    class Meta:
        """Meta."""

        model = Proveedor
        exclude = ('estado', 'representante_legal',
                   'enti_bancaria', 'num_cuenta',)
        Field = ('tipodoc', 'numdoc',
                 'direccion', 'telefono',
                 'email')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(ProveedorForm, self).__init__(*args, **kwargs)

        self.fields['razon_social'] = forms.CharField(
            label=capfirst(u'Nombres y Apellidos'),
            help_text=u'<small class="help-error"></small>'
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div(Field('razon_social', placeholder="Ingrese Nombres"),
                    css_class='col-md-4'),
                Div(Field('tipodoc'), css_class='col-md-4'),
                Div(Field('numdoc', placeholder="Ingrese un número"),
                    css_class='col-md-4'),
            ),
            Row(
                Div(Field('email', placeholder="Ingrese un correo"),
                    css_class='col-md-4'),
                Div(Field('direccion', placeholder="Ingrese un dirección"),
                    css_class='col-md-4'),
                Div(Field('telefono', placeholder="Ingrese un número"),
                    css_class='col-md-4'),
            ),
            Row(
                Div(Field('enti_bancaria', placeholder="Ingrese el nombre"),
                    css_class='col-md-4'),
                Div(Field('num_cuenta', placeholder="Ingrese un número"),
                    css_class='col-md-4'),
            ),
            Div(Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ), css_class='modal-footer',),
        )
