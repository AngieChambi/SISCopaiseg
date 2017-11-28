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

from ..models.historia import Historial, CARACTER, ACTIVIDAD, HABITAT, ALIMENTACION, APTITUP, CONVIVE
from ..models.mascota import Mascota, BOOL_GENERO, Cliente, CONDICION

class HistoriaForm(forms.ModelForm):
    """Tipo Documeto Form."""
    class Meta:
        """Meta."""
        model = Historial
        exclude = ()
        fields = ['num_historia','veterinario',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(HistoriaForm, self).__init__(*args, **kwargs)

        self.fields['num_historia'] = forms.CharField(
            label=capfirst(_(u'N° Historia:')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Div(Field('num_historia', css_class='input-required'),
                        css_class='col-md-6'),
                        Div(Field('veterinario', ),
                        css_class='col-md-6'),
                        ),
                    css_class='modal-body'
                    ),
                Div(
                    Row(
                        FormActions(
                            smtSave(),
                            btnCancel(),
                            btnReset(),
                            ),
                        ),
                    css_class='modal-footer '
                    ),
                css_class='modal-lg modal-dialog'
            ),
        )

class HistoriaMascotaForm(forms.ModelForm):

    """ """
    class Meta:
        model = Historial
        fields = ['num_historia',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(HistoriaMascotaForm, self).__init__(*args, **kwargs)

        self.fields['num_historia'] = forms.CharField(
            label=capfirst(_(u'N° Historia')),
            required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
            u' '),
        )

        self.fields['caracter'] = forms.ChoiceField(
            label=capfirst(_(u'caracter')), required=True,
            choices=CARACTER,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['actividad'] = forms.ChoiceField(
            label=capfirst(_(u'actividad')), required=True,
            choices=ACTIVIDAD,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['habitar'] = forms.ChoiceField(
            label=capfirst(_(u'habitar')), required=True,
            choices=HABITAT,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['alimentacion'] = forms.ChoiceField(
            label=capfirst(_(u'alimentacion')), required=True,
            choices=ALIMENTACION,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['aptitup'] = forms.ChoiceField(
            label=capfirst(_(u'aptitup')), required=True,
            choices=APTITUP,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['convive'] = forms.ChoiceField(
            label=capfirst(_(u'convive')), required=True,
            choices=CONVIVE,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['historia'] = forms.BooleanField(
            label=capfirst(_(u'historia')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical form-mascota'
        self. helper.layout = Layout(
            Field('person_id',),
                    Row(
                        Div(HTML('''<h2 class="subtitle-mascota">*Datos Personales:</h2>'''),
                        css_class="col-xs-12"),
                        Div(
                            Div(Field('num_historia', css_class='input-required form-control-mascota', placeholder="Ingrese el numero de Historia del paciente"),
                            css_class="col-md-3"),
                        css_class='col-md-12 div-mascota-forms'),
                    ),
                    Row(
                        Div(HTML('''<h2 class="subtitle-mascota">*Reseña del Paciente:</h2>'''),
                        css_class="col-xs-12"),
                        Div(
                            Div(Field('caracter', css_class='input-required'),
                            css_class='col-md-4'),
                            Div(Field('actividad', css_class='input-required'),
                            css_class='col-md-4'),
                            Div(Field('habitar', css_class='input-required'),
                            css_class='col-md-4'),
                            Row(
                                Div(
                                    Div(Field('alimentacion', css_class='input-required'),
                                    css_class='col-md-4'),
                                    Div(Field('aptitup', css_class='input-required'),
                                    css_class='col-md-4'),
                                    Div(InlineRadios('convive'),
                                    css_class='col-md-4'),
                                    Div(Field('historia', css_class='input-required'),
                                    css_class='estado-historia '),
                                css_class="col-md-12"),
                            ),
                        css_class="col-md-12 div-mascota-forms"),
                    ),
            Row(
                Div(
                    FormActions(
                        smtSave(),
                        btnCancel(),
                        btnReset(),
                    ),
                css_class="col-md-12 btn-controls"),
            ),
        )

class MascotaHistoriDetailForm(forms.ModelForm):
    class Meta:
        model = Historial
        fields = []
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(MascotaHistoriDetailForm, self).__init__(*args, **kwargs)

        self.fields['num_historia'] = forms.CharField(
            label=capfirst(_(u'num_historia')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['created_ath'] = forms.CharField(
            label=capfirst(_(u'created_ath')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['usuario'] = forms.CharField(
            label=capfirst(_(u'usuario')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['nombre'] = forms.CharField(
            label=capfirst(_(u'nombre')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['duenho'] = forms.ChoiceField(
            label=capfirst(_(u'duenho')), required=True,
            # widget=forms.RadioSelect(),

            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['direccion'] = forms.CharField(
            label=capfirst(_(u'direccion')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['direccion'] = forms.CharField(
            label=capfirst(_(u'direccion')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['direccion'] = forms.CharField(
            label=capfirst(_(u'direccion')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['ciudad'] = forms.CharField(
            label=capfirst(_(u'ciudad')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['telefono'] = forms.CharField(
            label=capfirst(_(u'telefono')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['edad'] = forms.CharField(
            label=capfirst(_(u'edad')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.fields['genero'] = forms.CharField(
            label=capfirst(_(u'genero')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['especie'] = forms.CharField(
            label=capfirst(_(u'especie')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['raza'] = forms.CharField(
            label=capfirst(_(u'raza')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.fields['color'] = forms.CharField(
            label=capfirst(_(u'color')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['actividad'] = forms.CharField(
            label=capfirst(_(u'actividad')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['alimentacion'] = forms.CharField(
            label=capfirst(_(u'alimentacion')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Informacion del Dueño'),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.duenho.label }} </label>
                                <div class="controls ">{{ form.duenho.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.direccion.label }} </label>
                                <div class="controls ">{{ form.direccion.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.ciudad.label }} </label>
                                <div class="controls ">{{ form.ciudad.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.telefono.label }} </label>
                                <div class="controls ">{{ form.telefono.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),

                ),
                Tab(
                    _('Informacion Mascota'),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.nombre.label }} </label>
                                <div class="controls ">{{ form.nombre.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.edad.label }} </label>
                                <div class="controls ">{{ form.edad.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.genero.label }} </label>
                                <div class="controls ">{{ form.genero.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.especie.label }} </label>
                                <div class="controls ">{{ form.especie.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.raza.label }} </label>
                                <div class="controls ">{{ form.raza.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.color.label }} </label>
                                <div class="controls ">{{ form.color.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                ),

                Tab(_('Historial'),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.num_historia.label }} </label>
                                <div class="controls ">{{ form.num_historia.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.created_ath.label }} </label>
                                <div class="controls ">{{ form.created_ath.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.usuario.label }} </label>
                                <div class="controls ">{{ form.usuario.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                ),
            ),
            Row(
                FormActions(
                    btnCancel(),
                ),
            ),
        )
