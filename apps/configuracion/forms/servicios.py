u"""Módulo Especie Form."""

from django import forms
from ..models.servicios import Servicios
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from crispy_forms.helper import FormHelper, Layout
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list


class ServiciosForm(forms.ModelForm):
    u"""Especie Form."""
    class Meta:
        """Meta."""
        model = Servicios
        fields = ('nombre', 'precio', 'descripcion',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(ServiciosForm, self).__init__(*args, **kwargs)

        self.fields['descripcion'] = forms.CharField(
                label=capfirst(_(u'Descripcion')), required=False,
                widget=forms.Textarea(attrs = {'rows': 4, }),
                help_text=u'<small class="help-error"></small> %s' % _(
                    u' '),
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Div(Field('nombre',  placeholder='Ingrese nombre del servicio',
                          css_class='input-required')),
                Div(Field('precio',
                  css_class='input-required')),
                  Div(Field('descripcion',)),
                FormActions(
                    smtSave(),
                ),
        )
