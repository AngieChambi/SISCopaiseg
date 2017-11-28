u"""Módulo Cita."""

from django import forms
from ..models.cita import Cita
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, StrictButton, FieldWithButtons
from crispy_forms.helper import FormHelper, Layout
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from apps.clinica.models.cliente import Cliente
from apps.sad.models import User

class CitaForm(forms.ModelForm):
    u"""Cita."""
    class Meta:
        """Meta."""
        model = Cita
        exclude = ('estado',)
        fields = ('descripcion', 'date',
                  'evento', 'veterinario', 'cliente')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(CitaForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['descripcion'] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'rows': 3, }),
        )
        self.fields['cliente'] = forms.ModelChoiceField(
            queryset=Cliente.objects.all(),
            empty_label=None,
            widget=forms.Select(
                attrs={'class': 'chosen-select',
                       'data-placeholder': 'Eliga el cliente'}),
        )
        self.fields['veterinario'] = forms.ModelChoiceField(
            queryset=User.objects.filter(is_veterinario=True),
            empty_label=None,
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div(Field('cliente',), css_class='col-md-6'),
                Div(Field('veterinario', ), css_class='col-md-6'),
            ),
            Row(
                Div(FieldWithButtons('evento', StrictButton(
                    "Agregar", id='addEvent')), css_class='col-md-6'),
                Div(Field('date',), css_class='col-md-6'),
            ),
            Row(
                Div(Field('descripcion',), css_class='col-md-12'),
            ),
        )
