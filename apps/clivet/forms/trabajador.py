u"""Módulo Trabajador Form."""

from django import forms
from apps.sad.models import User
from apps.params.models import IDENTITY_TYPE_CHOICES
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from crispy_forms.helper import FormHelper, Layout
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list


class TrabajadorForm(forms.ModelForm):
    u"""Trabajador Form."""
    nombre = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    numero = forms.IntegerField(required=False)
    tipo_documento = forms.ChoiceField(choices=IDENTITY_TYPE_CHOICES)
    fecha_de_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker', }),
        required=False)

    class Meta:
        """Meta."""
        model = User
        exclude = ()
        fields = ()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(TrabajadorForm, self).__init__(*args, **kwargs)
        self.fields['photo'] = forms.ImageField(
            label='', required=False,
            initial='persons/default.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'JPG, GIF, o PNG.'),
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div(Div(Field('photo'), css_class='text-center'),css_class='col-md-4'),
                Div(
                    Div(Field('nombre',  placeholder='Ingrese un nombre')),
                    Div(Field('apellidos', placeholder='Ingrese sus apellidos'),),
                    Div(Field('tipo_documento',),),
                    Div(Field('numero', placeholder='Ingrese un número'),),
                    Div(Field('fecha_de_nacimiento', placeholder='YYYY-MM-DD'),),

                    FormActions(
                        smtSave(),
                        btnCancel(),
                    ), css_class='col-md-8'),
            ),
        )
