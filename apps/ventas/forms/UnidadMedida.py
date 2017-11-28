from django import forms
from ..models.UnidadMedida import UnidadMedidaC
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, StrictButton, FieldWithButtons
from crispy_forms.helper import FormHelper, Layout
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list


class UnidadMedidaForm(forms.ModelForm):
    u"""Tipo Documeto Form."""

    class Meta:
        """Meta."""

        model = UnidadMedidaC
        exclude = ()
        Field = ('nombre', 'simbolo', 'cant_equivalencia',
                 'unidad_medida_venta')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(UnidadMedidaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Div(Field('nombre', placeholder="Ingrese un nombre"),
                            css_class='col-md-8'),
                        Div(Field('simbolo', placeholder="Ejem. Kg."),
                            css_class='col-md-4'),
                    ),
                    Row(
                        Div(Field(
                            'cant_equivalencia',
                            placeholder="Cant. de conversión"),
                            css_class='col-md-4'),
                        Div(FieldWithButtons('unidad_medida_venta',
                                             StrictButton(
                                                 "Agregar",
                                                 id='addUnidadV')),
                            css_class='col-md-8'),
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
