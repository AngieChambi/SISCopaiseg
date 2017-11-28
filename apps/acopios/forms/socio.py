from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row
from django import forms

from ..models.models.socio import Socio
from backengo.utils.forms import smtSave, btnCancel, btnReset


class SocioForm(forms.ModelForm):

    class Meta:
        """Meta."""

        model = Socio
        exclude = ('estado',)
        Field = ('cod_socio', 'direccion', 'ciudad',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(SocioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div(Field('cod_socio',
                          placeholder="Ingrese el nombre de la empresa"),
                    css_class='col-md-5'),
                Div(Field('tipodoc'), css_class='col-md-4'),
                Div(Field('numdoc', placeholder="Ingrese un número"),
                    css_class='col-md-3'),
            ),
            Row(
                Div(Field('representante_legal',
                          placeholder="Ingrese el nombre completo"),
                    css_class='col-md-5'),
                Div(Field('direccion', placeholder="Ingrese un dirección"),
                    css_class='col-md-4'),
                Div(Field('ciudad', placeholder="Ingrese un número"),
                    css_class='col-md-3'),
            ),
            Row(
                Div(Field('email', placeholder="Ingrese un correo"),
                    css_class='col-md-4'),
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
