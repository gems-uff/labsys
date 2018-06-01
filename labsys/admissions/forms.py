from flask_wtf import FlaskForm
import wtforms as wtf
import wtforms.widgets as widgets
import wtforms.widgets.html5 as html5widgets
from wtforms.validators import InputRequired, Optional, length
from labsys.utils.custom_fields import NullBooleanField

from . import custom_fields as cfields


class AddressForm(FlaskForm):
    ZONE_CHOICES = ((1, 'Urbana'),
                    (2, 'Rural'),
                    (3, 'Periurbana'),
                    (9, 'Ignorado'))

    class Meta:
        csrf = False

    country = wtf.StringField('País de residência',
                              validators=[length(max=128)])
    state = wtf.StringField('UF (Estado)',
                            validators=[length(max=2)])
    city = wtf.StringField('Município',
                           validators=[length(max=128)])
    neighborhood = wtf.StringField('Bairro',
                                   validators=[length(max=128)])
    zone = wtf.RadioField('Zona',
                          choices=ZONE_CHOICES,
                          default=9,
                          coerce=int, )
    details = wtf.StringField('Detalhes sobre residência',
                              validators=[length(max=255)])


class PatientForm(FlaskForm):
    AGE_UNIT_CHOICES = (
        ('Y', 'Anos'),
        ('M', 'Meses'),
        ('D', 'Dias'),
        ('H', 'Horas'))

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('I', 'Ignorado'))

    name = wtf.StringField('Nome do paciente')
    birth_date = wtf.DateField('Data de nascimento',
                               widget=html5widgets.DateInput(),
                               validators=[Optional()])
    age = wtf.IntegerField('Idade', validators=[Optional()])
    age_unit = wtf.RadioField('Tipo idade',
                              choices=AGE_UNIT_CHOICES,
                              default='Y',
                              coerce=str, )
    gender = wtf.RadioField('Sexo',
                            choices=GENDER_CHOICES,
                            default='I',
                            coerce=str, )
    residence = wtf.FormField(AddressForm, 'Residência')


class AdmissionForm(FlaskForm):
    id_lvrs_intern = wtf.StringField(
        'Número Interno', validators=[InputRequired()])
    first_symptoms_date = wtf.DateField('Data dos primeiros sintomas',
                                        widget=html5widgets.DateInput(),
                                        validators=[InputRequired()])
    semepi_symptom = wtf.IntegerField('Semana Epidemiológica (Sintomas)',
                                      validators=[Optional()])
    state = wtf.StringField('UF (Estado)',
                            validators=[length(max=2)])
    city = wtf.StringField('Município de registro do caso',
                           validators=[length(max=128)])
    health_unit = wtf.StringField('Unidade de Saúde')
    requesting_institution = wtf.StringField('Instituição Solicitante')
    details = wtf.StringField('Informações Adicionais',
                              widget=widgets.TextArea())
    patient = wtf.FormField(PatientForm, 'Dados do Paciente')
    submit = wtf.SubmitField('Salvar')


class DatedEventForm(FlaskForm):
    def __init__(self, occurred_label='Ocorreu', date_label='Data', **kwargs):
        csrf_enabled = kwargs.pop('csrf_enabled', False)
        super().__init__(csrf_enabled=csrf_enabled, **kwargs)
        self.occurred.label.text = occurred_label
        self.date.label.text = date_label

    occurred = NullBooleanField(default=None)
    # TODO: make date required if occurred is True (maybe on route)
    date = wtf.DateField(widget=html5widgets.DateInput(),
                         validators=[Optional()])


class VaccineForm(DatedEventForm):
    def __init__(self, **kwargs):
        super().__init__(occurred_label='Houve aplicação?',
                         date_label='Data da última dose', **kwargs)


class HospitalizationForm(DatedEventForm):
    def __init__(self, **kwargs):
        super().__init__(occurred_label='Ocorreu internação?',
                         date_label='Data de internação(entrada)', **kwargs)


class UTIHospitalizationForm(DatedEventForm):
    def __init__(self, **kwargs):
        super().__init__(occurred_label='Foi internado em UTI?',
                         date_label='Data de internação (entrada)', **kwargs)


class ClinicalEvolutionForm(DatedEventForm):
    def __init__(self, **kwargs):
        super().__init__(occurred_label='Evoluiu para óbito?',
                         date_label='Data do óbito', **kwargs)


class DatedEventFormGroup(FlaskForm):
    vaccine = wtf.FormField(VaccineForm, 'Vacina contra gripe')
    hospitalization = wtf.FormField(HospitalizationForm,
                                    'Internação Hospitalar')
    uti_hospitalization = wtf.FormField(UTIHospitalizationForm,
                                        'Internação UTI')
    clinical_evolution = wtf.FormField(ClinicalEvolutionForm,
                                       'Evolução Clínica')
    submit = wtf.SubmitField('Salvar')


class ObservedSymptomForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)
        self.observed.label = wtf.Label(
            self.observed.id,
            kwargs.pop('symptom_name', 'UNDEFINED'))

    symptom_id = wtf.IntegerField(widget=widgets.HiddenInput())
    observed = NullBooleanField()
    details = wtf.StringField(validators=[length(max=128)],
                              render_kw={'placeholder': 'observações'})


class ObservedSymptomFormList(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    primary = wtf.FieldList(
        wtf.FormField(form_class=ObservedSymptomForm),
        'Primários')
    secondary = wtf.TextField(
        'Secundários (separar por vírgula)',
        validators=[Optional()],
        render_kw={'placeholder': 'Ex.: tosse, desmaios, febre (40 graus)'})
    submit = wtf.SubmitField('Salvar')


class ObservedRiskFactorForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)
        self.observed.label = wtf.Label(
            self.observed.id,
            kwargs.pop('risk_factor_name', 'UNDEFINED'))

    risk_factor_id = wtf.IntegerField(widget=widgets.HiddenInput())
    observed = NullBooleanField()
    details = wtf.StringField(validators=[length(max=128)],
                              render_kw={'placeholder': 'observações'})


class ObservedRiskFactorFormList(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    primary = wtf.FieldList(
        wtf.FormField(form_class=ObservedRiskFactorForm),
        'Primários')
    secondary = wtf.TextField(
        'Secundários (separar por vírgula)',
        validators=[Optional()],
        render_kw={'placeholder': 'Ex.: obesidade'})
    submit = wtf.SubmitField('Salvar')


class CdcExamForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)

    FLU_TYPE_CHOICES = (('A', 'A'),
                        ('B', 'B'),
                        ('Inconclusivo', 'Inconclusivo'),
                        ('Não Realizado', 'Não Realizado'),
                        ('Ignorado', 'Ignorado'))
    FLU_SUBTYPE_CHOICES = (('H1', 'H1'),
                           ('H3', 'H3'),
                           ('Victoria', 'Victoria'),
                           ('Yamagata', 'Yamagata'),
                           ('Não Subtipado', 'Não SubtipADO'),
                           ('Não Subtipável', 'Não SubtipÁVEL'),
                           ('Ignorado', 'Ignorado'))

    flu_type = wtf.SelectField('Tipagem',
                               choices=FLU_TYPE_CHOICES,
                               default='Ignorado',
                               coerce=str, )
    flu_subtype = wtf.SelectField('Subtipo OU Linhagem',
                                  choices=FLU_SUBTYPE_CHOICES,
                                  default='Ignorado',
                                  coerce=str, )
    dominant_ct = wtf.FloatField('CT (principal)', validators=[Optional()])
    dominant_ct = wtf.FloatField(
        'CT (principal)',
        render_kw={'placeholder': 'Ex.: 20.50'},
        validators=[Optional()],
        widget=html5widgets.NumberInput(step='0.01', min='0.00', max='99999.99'))
    details = wtf.StringField(
        'Informações adicionais sobre exame', validators=[length(max=128)],
        widget=widgets.TextArea())


class SampleForm(FlaskForm):
    collection_date = wtf.DateField('Data de coleta',
                                    widget=html5widgets.DateInput(),
                                    validators=[InputRequired()])
    semepi = wtf.IntegerField(
        'Semana Epidemiológica (Coleta)', validators=[Optional()])
    admission_date = wtf.DateField('Data de Entrada no LVRS',
                                   widget=html5widgets.DateInput(),
                                   validators=[InputRequired()])
    details = wtf.StringField('Informações adicionais')
    method_id = cfields.MethodSelectField()
    cdc_exam = wtf.FormField(label='Resultado Exame CDC',
                             form_class=CdcExamForm)
    submit = wtf.SubmitField('Adicionar amostra')


# TODO: normalize it (creating a separate tabel for models)
class AntiviralForm(FlaskForm):
    ANTIVIRAL_CHOICES = (
        ('1 - Não usou', '1 - Não usou'),
        ('2 - Oseltamivir', '2 - Oseltamivir'),
        ('3 - Zanamivir', '3 - Zanamivir'),
        ('9 - Ignorado', '9 - Ignorado'),
    )

    def __init__(self, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)

    usage = wtf.SelectField('Uso de antiviral?',
                            choices=ANTIVIRAL_CHOICES,
                            default='9 - Ignorado',
                            coerce=str, )
    other = wtf.StringField('4 - Outro, especifique')
    start_date = wtf.DateField('Início do tratamento',
                               widget=html5widgets.DateInput(),
                               validators=[Optional()])
    submit = wtf.SubmitField('Salvar')


# TODO: normalize it (creating a separate tabel for models)
class XRayForm(FlaskForm):
    XRAY_CHOICES = (
        ('1 - Normal', '1 - Normal'),
        ('2 - Infiltrado intersticial', '2 - Infiltrado intersticial'),
        ('3 - Consolidação', '3 - Consolidação'),
        ('4 - Misto', '4 - Misto'),
        ('6 - Não realizado', '6 - Não realizado'),
        ('9 - Ignorado', '9 - Ignorado'),
    )

    def __init__(self, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)

    usage = wtf.SelectField('Raio X de Tórax',
                            choices=XRAY_CHOICES,
                            default='9 - Ignorado',
                            coerce=str, )
    other = wtf.StringField('5 - Outro, especifique')
    start_date = wtf.DateField('Data do Raio X',
                               widget=html5widgets.DateInput(),
                               validators=[Optional()])
    submit = wtf.SubmitField('Salvar')
