from django import forms
from ..models.acopio import Acopio
from apps.params.models import IDENTITY_TYPE_CHOICES


class AcopioForm(forms.ModelForm):
    u"""Tipo Documeto Form."""

    producto = forms.CharField(label="", required=False,
                               widget=forms.TextInput(attrs={'type': 'search', 'class': 'form-control typeahead input-lg', 'placeholder': 'Buscar Producto ', 'autofocus': 'autofocus'}))
    data_compra = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'type': 'hidden'}))

    # =====================modal==========================
    tipo_doc = forms.ChoiceField(
        choices=IDENTITY_TYPE_CHOICES, required=False,
        label='Tipo de documento')

    class Meta:

        model = Acopio
        fields = ('total', 'socio', 'n_ticket')
        exclude = ()
        widgets = {
            'socio': forms.Select(
                attrs={'class': 'chosen-select',
                       'data-placeholder': 'Choose a Country', 'style': 'width: 100%;height:34px;'}),
            'total': forms.TextInput(attrs={'class': 'form-control text-left'}),
            'n_ticket': forms.ClearableFileInput()}

    def __init__(self, *args, **kwargs):
        super(AcopioForm, self).__init__(*args, **kwargs)
        self.fields['socio'].empty_label = 'Buscar...'
