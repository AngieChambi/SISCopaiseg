#encoding: utf-8
from django import forms

from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.text import capfirst, get_text_list
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, \
    PrependedAppendedText, PrependedText, InlineRadios

from django.utils.timezone import get_current_timezone
from datetime import datetime

from backengo.utils.forms import smtSave, btnCancel, btnReset
from ..models.historia import CARACTER, ACTIVIDAD, HABITAT, ALIMENTACION, APTITUP, CONVIVE
from ..models.mascota import Mascota, BOOL_GENERO, Cliente, CONDICION

class MascotaForm(forms.ModelForm):
    """Tipo Documeto Form."""
    class Meta:
        """Meta."""
        model = Mascota
        exclude = ('duenho',)
        fields = ['nombre','fecha_nacimiento','genero','especie','raza','color','descripcion',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(MascotaForm, self).__init__(*args, **kwargs)

        self.fields['nombre'] = forms.CharField(
            label=capfirst(_(u'nombre')),
            required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
            u' '),
        )
        self.fields['fecha_nacimiento'] = forms.DateTimeField(
            label=_(u'Fecha Nacimiento'), required=False,
            initial=datetime.now().replace(tzinfo=get_current_timezone()),
            widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',),
            input_formats=(
                '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S'),
            help_text=u'<small class="help-error"></small> %s' % _(
                u''),
        )
        self.fields['genero'] = forms.ChoiceField(
            label=capfirst(_(u'genero*:')), required=False,
            choices=BOOL_GENERO,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['esterelizado'] = forms.BooleanField(
            label=capfirst(_(u'¿Esterelizado?')),
            required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['cond_corporal'] = forms.ChoiceField(
            label=capfirst(_(u'C. Corporal')), required=False,
            choices=CONDICION,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.fields['descripcion'] = forms.CharField(
            label=capfirst(_(u'Descripcion')), required=False,
            widget=forms.Textarea(attrs = {'rows': 4, }),

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

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self. helper.layout = Layout(
                    HTML("""<!-- #section:plugins/fuelux.wizard --><div id="fuelux-wizard-container">"""),
                    HTML("""
                        <div><!-- #section:plugins/fuelux.wizard.steps -->
                            <ul class="steps">
                                <li data-step="1" class="active">
                                    <span class="step">1</span>
                                    <span class="title">Datos Generales</span>
                                </li>
                                <li data-step="2">
                                    <span class="step">2</span>
                                    <span class="title">Caracteristicas</span>
                                </li>
                                <li data-step="3">
                                    <span class="step">3</span>
                                    <span class="title">Reseña del Paciente</span>
                                </li>

                                <li data-step="4">
                                    <span class="step">4</span>
                                    <span class="title">Otra Informacion</span>
                                </li>
                            </ul><!-- /section:plugins/fuelux.wizard.steps -->
                        </div>
                        <hr />"""),
                    HTML("""<!-- #section:plugins/fuelux.wizard.container --><div class="step-content pos-rel">"""),
                    HTML(""" <div class="step-pane active" data-step="1">"""),
                        Row(
                            Div(
                                Field('nombre', placeholder="Introdusca el nombre de la mascota", css_class='input-required'),
                            css_class="col-md-6"),
                            Div(
                                Field('fecha_nacimiento', css_class='input-datex'),
                            css_class="col-md-6"),
                        ),
                        Row(
                            Div(
                                Field('genero', default="macho"),
                            css_class="col-md-6"),

                            Div(
                                Field('cond_corporal', ),
                            css_class="col-md-4"),
                            HTML("""<div class="col-xs-2">"""),
                                HTML("""<div id="div_id_esterelizado" class="form-group">"""),
                                HTML("""<label>{{form.esterelizado.label}}</label>"""),
                                HTML("""<div    class="controls">{{form.esterelizado}}<span class="lbl"></span></div>"""),
                            HTML("""</div></div>"""),

                        ),
                    HTML("""</div>"""),
                    HTML(""" <div class="step-pane" data-step="2">"""),
                        Row(
                            Div(
                                Field('especie',),
                            css_class="col-md-4"),
                            Div(
                                Field('raza',),
                            css_class="col-md-4"),
                            Div(
                                Field('color',),
                            css_class="col-md-4"),
                        ),
                    HTML("""</div>"""),
                    HTML(""" <div class="step-pane" data-step="3">"""),
                    Row(
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
                                    Div(Field('convive'),
                                    css_class='col-md-4'),
                                css_class="col-md-12"),
                            ),
                        css_class="col-md-12 div-mascota-forms"),
                    ),
                    HTML("""</div>"""),
                    HTML(""" <div class="step-pane" data-step="4">"""),
                    Div(
                        Field('descripcion', placeholder="Introdusca una cualidad de la mascota"),
                        css_class='col-md-12'),
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
class MascotaUpdateForm(forms.ModelForm):
    """Tipo Documeto Form."""

    class Meta:
        """Meta."""
        model = Mascota
        exclude = ('duenho',)
        fields = ['nombre','fecha_nacimiento','genero','especie','raza','color','descripcion',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(MascotaUpdateForm, self).__init__(*args, **kwargs)

        self.fields['nombre'] = forms.CharField(
            label=capfirst(_(u'nombre')),
            required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
            u' '),
        )

        self.fields['fecha_nacimiento'] = forms.DateTimeField(
            label=_(u'Fecha Nacimiento'), required=False,
            initial=datetime.now().replace(tzinfo=get_current_timezone()),
            widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',),
            input_formats=(
                '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S'),
            help_text=u'<small class="help-error"></small> %s' % _(
                u''),
        )
        self.fields['genero'] = forms.ChoiceField(
            label=capfirst(_(u'genero*:')), required=False,
            choices=BOOL_GENERO,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['esterelizado'] = forms.BooleanField(
            label=capfirst(_(u'¿Esterelizado?')),
            required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['cond_corporal'] = forms.ChoiceField(
            label=capfirst(_(u'C. Corporal')), required=False,
            choices=CONDICION,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.fields['descripcion'] = forms.CharField(
            label=capfirst(_(u'Descripcion')), required=False,
            widget=forms.Textarea(attrs = {'rows': 4, }),

            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )


        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self. helper.layout = Layout(
            Row(
                Div(
                    Field('nombre', placeholder="Introdusca el nombre de la mascota", css_class='input-required'),
                    css_class="col-md-4"),
                Div(
                    Field('fecha_nacimiento', css_class='date-picker'),
                css_class="col-md-4"),
                    Div(
                        Field('genero', default="macho"),
                    css_class="col-md-4"),
            ),
                        Row(
                            Div(
                                Field('especie',),
                            css_class="col-md-4"),

                            Div(
                                Field('raza',),
                            css_class="col-md-4"),
                            Div(
                                Field('color',),
                            css_class="col-md-4"),
                    Div(
                        Field('descripcion', placeholder="Introdusca una cualidad de la mascota"),
                        css_class='col-md-12'),
                        ),
        )
