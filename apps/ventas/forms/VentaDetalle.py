from django import forms
from ..models.Venta_Detalle import Detalle_Venta


class Detalle_VentaForm(forms.ModelForm):
    u"""Tipo Documeto Form."""
    class Meta:
        """Meta."""
        model = Detalle_Venta
        fileds = ('producto',)
        exclude = ()
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
        }
