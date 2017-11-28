from django import forms
from ..models.Producto import Producto
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, StrictButton, FieldWithButtons
from crispy_forms.helper import FormHelper, Layout
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from apps.ventas.models.Departamento import Departamento
from apps.ventas.models.UnidadMedida import UnidadMedidaV


class ProductoForm(forms.ModelForm):
    u"""Tipo Documeto Form."""
    # =====================modal==========================
    categoria_departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
        label='Departamento',
        widget=forms.Select(attrs={'class': 'form-control'}))
    unidadc_ventas = forms.ModelChoiceField(
        queryset=UnidadMedidaV.objects.all(),
        required=False,
        label='Unidad de medida de ventas',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        """Meta."""
        model = Producto
        exclude = ('existencia', 'MontoReal', 'igv')
        fields = ('nombre', 'codigo', 'categoria',
                  'fechaVencimiento', 'unidad_medida', 'precioV', 'precioC')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div(Field('nombre', placeholder="username"),
                    css_class='col-md-6'),
                Div(Field('codigo', placeholder="username"),
                    css_class='col-md-3'),
                Div(Field('fechaVencimiento', placeholder="YYYY-MM-DD"),
                    css_class='col-md-3'),
            ),
            Row(
                Div(FieldWithButtons('categoria', StrictButton(
                    "Agregar", id='addCategoria')), css_class='col-md-4'),
                Div(FieldWithButtons('unidad_medida', StrictButton(
                    "Agregar", id='addUnidad')), css_class='col-md-4'),
                Div(Field('precioC', placeholder="username"),
                    css_class='col-md-2'),
                Div(Field('precioV', placeholder="username"),
                    css_class='col-md-2'),
            ),
            Div(Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ), css_class='modal-footer',),
        )
