#encoding: utf-8
from django import forms

from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst, get_text_list
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, InlineRadios, InlineCheckboxes

from backengo.utils.forms import smtSave, btnCancel, btnReset

from django.utils.timezone import get_current_timezone
from datetime import datetime

from ..models.atenciones import Atenciones, ArchivosAdjuntos

class AtencionesForm(forms.ModelForm):
    """Tipo Documeto Form."""
    class Meta:
        """Meta."""
        model = Atenciones
        exclude = ('colamedica',)
        fields = []
