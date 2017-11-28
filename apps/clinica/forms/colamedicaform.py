#encoding: utf-8
from django import forms

from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst, get_text_list
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, StrictButton
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.timezone import get_current_timezone
from datetime import datetime
from ..models.colamedica import ColaMedica
from ..models.mascota import Mascota
from apps.clinica.models.cliente import Cliente
from apps.sad.models import User

class ColaMedicaForm(forms.ModelForm):
    """Tipo Documeto Form."""
    cliente = forms.ModelChoiceField(
            queryset=Cliente.objects.all(), required=False, )

    mascotas = forms.ModelChoiceField(
            queryset=Mascota.objects.all(), required=False, )
    class Meta:
        """Meta."""
        model = ColaMedica
        exclude = ()
        fields = ['fuente_atencion','mascota','descripcion','medico',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(ColaMedicaForm, self).__init__(*args, **kwargs)

        self.fields['descripcion'] = forms.CharField(
            label=capfirst(_(u'Descripcion:')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['medico'] = forms.ModelChoiceField(
                    queryset=User.objects.filter(groups=10), required=False, )
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate'
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('mascota',  css_class='input-required', readonly=True),
                        css_class="col-md-4"),
                Div(
                    Field('medico', css_class='input-required'),
                        css_class="col-md-4"),
                Div(
                    Field('fuente_atencion', placeholder="Introdusca el color", css_class='input-required'),
                        css_class="col-md-4"),
                Div(
                    Field('descripcion', ),
                        css_class="col-md-12"),
            ),
            Row(
                Div(
                    FormActions(
                        smtSave(),
                    ),
                css_class="col-md-12 btn-controls"),
            ),
        )
