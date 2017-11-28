#encoding: utf-8
from django import forms
from django_bootstrap_typeahead.fields import *
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst, get_text_list
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML, Submit
from crispy_forms.bootstrap import FormActions, TabHolder, Tab,  PrependedText, Accordion,  AccordionGroup, StrictButton, AppendedText
from backengo.utils.forms import smtSave, btnCancel, btnReset
from django.utils.timezone import get_current_timezone
from datetime import datetime
from django.utils import timezone
from ..models.atencion import Atencion
from ..models.consulta import HallasgosClinicos

class AtencionForm(forms.ModelForm):

    class Meta:
        """Meta."""
        model = Atencion
        exclude = ('colamedica', 'historia',)
        fields = ['temperatura', 'fc', 'fr', 'kg', 'porcentaje', 'tlc', 'anamnesis', 'dx', 'hallasgos_clinicos', 'motivo_atencion', 'observacion', 'pronostico', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(AtencionForm, self).__init__(*args, **kwargs)



        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(

        Row(
        Div(Field('motivo_atencion', css_class="input-required"),
        css_class='col-md-12'),
        ),
            Row(
                Div(Field('temperatura', css_class='input-required'),
                    css_class='col-md-2'),
                Div(Field('fc', css_class="input-required"),
                    css_class='col-md-2'),
                Div(Field('fr', css_class='input-required'),
                    css_class='col-md-2'),
                Div(Field('kg', css_class='input-required'),
                    css_class='col-md-2'),
                Div(Field('porcentaje', css_class='input-required'),
                    css_class='col-md-2'),
                Div(Field('tlc', css_class='input-required'),
                    css_class='col-md-2'),

            ),
            Row(
                Div(Field('anamnesis'),
                    css_class='col-md-12'),
            ),
            Row(
                Div(Field('hallasgos_clinicos'),
                    css_class='col-md-12'),
            ),
            Row(
                Div(Field('diagnostico'),
                    css_class='col-md-12'),
            ),
            Row(
                Div(Field('dx'),
                    css_class='col-md-12'),
            ),
            Row(
                Div(Field('pronostico'),
                    css_class='col-md-12'),
            ),
            Row(
                Div(Field('pruebas_auxiliares'),
                    css_class='col-md-12'),
            ),
            Row(
                Div(Field('tratamiento'),
                    css_class='col-md-12'),
            ),
            Row(
                Div(Field('observacion'),
                    css_class='col-md-12'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class ConsultaForm(forms.ModelForm):
    """ """
    atenciones_id = forms.CharField(widget=forms.HiddenInput(), required=False,)
    data_diagnostico = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'type': 'hidden',}))
    tipo_diagnostico = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'type': 'hidden', 'value':'Afirmativo'}))

    class Meta:
        model = Atencion
        exclude = ('atenciones', 'dx')
        fields = ['temperatura', 'fc', 'fr', 'kg', 'porcentaje', 'tlc', 'anamnesis',  'dx',  'motivo_atencion', 'observacion', 'pronostico', 'data_diagnostico',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(ConsultaForm, self).__init__(*args, **kwargs)

        self.fields['motivo_atencion'] = forms.CharField(
            widget=forms.Textarea(attrs={"rows" : 2}),
            label=capfirst(_(u'Motivo de atención')),
            required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )

        self.fields['anamnesis'] = forms.CharField(
            widget=forms.Textarea(attrs={"rows" : 2}),
            label=capfirst(_(u'Anamnesis y Discripción')),
            required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )
        self.fields['pronostico'] = forms.CharField(
            label=capfirst(_(u'Pronostico')),
            required=False,
        )
        self.fields['temperatura'] = forms.CharField(
            label=False, required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )
        self.fields['fc'] = forms.CharField(
            label=False, required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )
        self.fields['fr'] = forms.CharField(
            label=False, required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )
        self.fields['kg'] = forms.CharField(
            label=False, required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )
        self.fields['porcentaje'] = forms.CharField(
            label=False, required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )
        self.fields['tlc'] = forms.CharField(
            label=False, required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                        u' '),
        )

        self.fields['hallasgos_clinicos'] = forms.ModelMultipleChoiceField(
        queryset=HallasgosClinicos.objects.all(), label=False, required=False,
        help_text=u'<small class="help-error"></small> %s' % (
        u' '
        ))
        self.fields['diagnosticos'] = forms.CharField()
        self.fields['prueba_auxiliar'] = forms.CharField()
        self.fields['tratamientos'] = forms.CharField()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate validation-form form-vertical'
        self. helper.layout = Layout(
            Field('atenciones_id',),
            HTML("""<!-- #section:plugins/fuelux.wizard --><div id="fuelux-wizard-container">"""),
            HTML("""
                <div><!-- #section:plugins/fuelux.wizard.steps -->
                    <ul class="steps">
                        <li data-step="1" class="active">
                            <span class="step">1</span>
                            <span class="title">Constantes Biológicas</span>
                        </li>
                        <li data-step="2">
                            <span class="step">2</span>
                            <span class="title">Hallasgos Clinicos</span>
                        </li>

                        <li data-step="3">
                            <span class="step">3</span>
                            <span class="title">Diagnosticar</span>
                        </li>

                        <li data-step="4">
                            <span class="step">4</span>
                            <span class="title">Tratamiento</span>
                        </li>
                    </ul><!-- /section:plugins/fuelux.wizard.steps -->
                </div>
                <hr />"""),
            HTML("""<!-- #section:plugins/fuelux.wizard.container --><div class="step-content pos-rel">"""),
            HTML(""" <div class="step-pane active" data-step="1">"""),
                Row(
                    Div(
                        Field('motivo_atencion', placeholder= '¿Por qué le estas trayendo a la mascota?', css_class="input-required"),
                    css_class='col-md-12'),
                    Div(Field('anamnesis', css_class='input-required'),
                                            css_class='col-md-12'),
                    Div(
                        PrependedText('temperatura', 'T°', placeholder="Temperatura",       css_class='input-required', ),
                    css_class='col-md-2'),
                    Div(
                        PrependedText('fc', 'FC', placeholder="Frec. Cardiaca",css_class='input-required'),
                    css_class='col-md-2'),
                    Div(
                        PrependedText('fr', 'FR', placeholder="Frec. Respiratoria",css_class='input-required'),
                    css_class='col-md-2'),
                    Div(
                        PrependedText('kg', 'Kg', placeholder="Peso de Mascota", css_class='input-required'),
                    css_class='col-md-2'),
                    Div(
                        PrependedText('porcentaje', '%', placeholder="Porcentaje",css_class='input-required'),
                    css_class='col-md-2'),
                    Div(
                        PrependedText('tlc', 'TLC', placeholder="TLC", css_class='input-required'),
                    css_class='col-md-2'),
                    ),
            HTML("""</div>"""),
            HTML(""" <div class="step-pane" data-step="2">"""),
                Row(
                    Div(Field('hallasgos_clinicos',size="5" ),
                        css_class='col-md-12'),
                ),
            HTML("""</div>"""),
            HTML(""" <div class="step-pane" data-step="3">"""),

            Row(
                Div(
                    Field('diagnosticos'),
                    HTML('<table class="table table-bordered panel panel-default table-responsive"><tbody id="datos_diagnostico" class="panel-heading"></tbody></table>'),
                css_class='col-md-6'),

                Div(
                    Field('prueba_auxiliar'),
                    HTML('<table class="table table-bordered panel panel-default table-responsive"><tbody id="datos_pruebas" class="panel-heading"></tbody></table>'),
                css_class='col-md-6'),
            ),
                Row(
                    Div(Field('pronostico'),
                        css_class='col-md-12'),
                ),
            HTML("""</div>"""),
            HTML(""" <div class="step-pane" data-step="4">"""),
                Row(
                    Div(Field('tratamientos'),
                        css_class='col-md-12'),
                    Div(HTML('<table class="table table-bordered panel panel-default table-responsive"><tbody id="datos_tratamiento" class="panel-heading"></tbody></table>'),
                            css_class='col-md-12'),
                ),
                Row(
                    Div(Field('observacion'),
                        css_class='col-md-12'),
                ),
            HTML("""</div></div></div>
                        <hr />
                        <div class="wizard-actions">
                            <!-- #section:plugins/fuelux.wizard.buttons -->
                            <a class="btn btn-prev" id="prev" data-last="Inicio">
                                <i class="ace-icon fa fa-arrow-left"></i>
                                Prev
                            </a>
                            <a type="button" name="cancel" class="btn btn btn-danger btn-back" id="button-id-cancel" title="Cancel">
                                <i class="btn-icon-onlyx fa fa-ban"></i> <span class="hidden-xs"> Cancel</span>
                            </a>
                            <button type="submit" name="submit" class="btn btn-primary text-bold" id="submit-id-submit" title="Grabar">
                                <i class="btn-icon-onlyx fa fa-save"></i> <span class="hidden-xsx"> Grabar</span>
                            </button>
                            <a class="btn btn-success btn-next" id="next" data-last="Finish">
                                Next
                                <i class="ace-icon fa fa-arrow-right icon-on-right"></i>
                            </a>
                            <!-- /section:plugins/fuelux.wizard.buttons -->
                        </div><!-- /section:plugins/fuelux.wizard -->"""),
        )

class AtencionMascotaDetailForm(forms.ModelForm):
    """ """
    class Meta:
        model = Atencion
        exclude= []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(AtencionMascotaDetailForm, self).__init__(*args, **kwargs)

        self.fields['num_historia'] = forms.CharField(
            label=capfirst(_(u'N° Historia')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['veterinario'] = forms.CharField(
            label=capfirst(_(u'veterinario')), required=True,
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


        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Perfil'),
                    Row(
                        Div(Div(HTML('''
                                <img src="/media/clivet/images.jpg"" alt="{{ form.nombre.value}}" class="img-responsive">
                                '''),
                                Div(HTML('''
                                    <h3>{{ form.nombre.value}}</h3>
                                    <p><strong>{{ form.num_historia.label }}</strong>: {{ form.num_historia.value}}</p>
                                    <button type="button" class="btn btn-info btn-lg">
                                        <i class="fa fa-calendar" aria-hidden="true"></i>
                                    </button>
                                    <button type="button" class="btn btn-warning btn-lg">
                                        <i class="fa fa-hospital-o" aria-hidden="true"></i>
                                    </button>
                                    '''
                                    ),
                                css_class='caption text-center'),
                                css_class='thumbnail'),
                            css_class='col-md-6 col-md-3 '),
                        Div(HTML('''
                                {% include "clinica/includes/tablaperfil.html" %}
                                '''),
                            css_class='col-md-5 panel panel-default'),
                        Div(HTML('''
                                {% include "clinica/includes/tablasreport.html" %}
                                '''),
                            css_class='col-md-4'),
                    ),
                ),
                Tab(_('Historial de Compras'),
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
                                <label class="control-label"> {{ form.veterinario.label }} </label>
                                <div class="controls ">{{ form.veterinario.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                ),
                Tab(_('Historia Clinico'),
                    Row(
                        Div(HTML('''
                                 {% include "clinica/includes/atencion.html" %}
                                 '''
                                 ),
                            ),
                        ),
                ),
                Tab(_('Agenda Medica'),
                ),
            ),
        )
