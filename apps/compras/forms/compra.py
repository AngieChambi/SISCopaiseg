from django import forms
from ..models.compra import Compra
from apps.compras.models.Proveedor import Tipo_Documento


class CompraForm(forms.ModelForm):
    u"""Tipo Documeto Form."""

    producto = forms.CharField(label="", required=False,
                               widget=forms.TextInput(attrs={'type': 'search', 'class': 'form-control typeahead input-lg', 'placeholder': 'Buscar Producto ', 'autofocus': 'autofocus'}))
    data_compra = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'type': 'hidden'}))

    # =====================modal==========================
    tipo_doc = forms.ChoiceField(
        choices=Tipo_Documento, required=False,
        label='Tipo de documento')

    class Meta:

        model = Compra
        fields = ('total', 'proveedor', 'comprobante')
        exclude = ()
        widgets = {
            'proveedor': forms.Select(
                attrs={'class': 'chosen-select',
                       'data-placeholder': 'Choose a Country','style':'width: 100%;height:34px;'}),
            'total': forms.TextInput(attrs={'class': 'form-control text-left'}),
            'comprobante': forms.ClearableFileInput()}

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].empty_label = 'Buscar...'
