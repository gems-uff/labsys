from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, FieldList, FloatField, FormField,
                     IntegerField, Label, RadioField, SelectField, StringField,
                     SubmitField, widgets)
from wtforms.validators import InputRequired, Optional, length
from . import custom_fields as cfields


ZONE_CHOICES = ((1, 'Urbana'),
                (2, 'Rural'),
                (3, 'Periurbana'),
                (9, 'Ignorado'))

YES_NO_IGNORED_CHOICES = ((1, 'Sim'),
                          (0, 'Nao'),
                          (9, 'Ignorado'))


AGE_UNIT_CHOICES = (('Y', 'Anos'),
                    ('M', 'Meses'),
                    ('D', 'Dias'),
                    ('H', 'Horas'))

GENDER_CHOICES = (('M', 'Masculino'),
                  ('F', 'Feminino'),
                  ('I', 'Ignorado'))


class AddressForm(FlaskForm):
    class Meta:
        csrf = False

    country = StringField(label='País de residência',
                          validators=[length(max=128)])
    state = StringField(label='UF (Estado)',
                        validators=[length(max=2)])
    city = StringField(label='Município',
                       validators=[length(max=128)])
    neighborhood = StringField(label='Bairro',
                               validators=[length(max=128)])
    zone = RadioField(
        label='Zona',
        choices=ZONE_CHOICES,
        default=9,
        coerce=int, )
    details = StringField(label='Observações', validators=[length(max=255)])


class PatientForm(FlaskForm):
    name = StringField('Nome do paciente')
    birth_date = DateField(
        'Data de nascimento', format='%d/%m/%Y', validators=[Optional()])
    age = IntegerField('Idade', validators=[Optional()])
    age_unit = RadioField(
        label='Tipo idade',
        choices=AGE_UNIT_CHOICES,
        default='Y',
        coerce=str, )
    gender = RadioField(
        label='Sexo',
        choices=GENDER_CHOICES,
        default='I',
        coerce=str, )
    residence = FormField(AddressForm, label='Residência')


class VaccineForm(FlaskForm):
    class Meta:
        csrf = False

    occurred = RadioField(
        label='Aplicação',
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int, )
    date = DateField(
        label='Data da última dose',
        format='%d/%m/%Y',
        validators=[Optional()])


class HospitalizationForm(FlaskForm):
    class Meta:
        csrf = False

    occurred = RadioField(
        label='Ocorreu internação?',
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int, )
    date = DateField(
        label='Data de internação (entrada)',
        format='%d/%m/%Y',
        validators=[Optional()])


class UTIHospitalizationForm(FlaskForm):
    class Meta:
        csrf = False

    occurred = RadioField(
        label='Foi internado em UTI?',
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int, )
    date = DateField(
        label='Data de internação (entrada)',
        format='%d/%m/%Y',
        validators=[Optional()])


class ClinicalEvolutionForm(FlaskForm):
    class Meta:
        csrf = False

    occurred = RadioField(
        label='Evoluiu para óbito?',
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int, )
    date = DateField(
        label='Data do óbito',
        format='%d/%m/%Y',
        validators=[Optional()])


class ObservedSymptomForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)
        self.observed.label = Label(self.observed.id,
                                    kwargs.pop('symptom_name', 'Undefined'))

    symptom_id = IntegerField(widget=widgets.HiddenInput())
    observed = RadioField(
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int, )
    details = StringField(validators=[length(max=128)])


class SecondarySymptomForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(
            csrf_enabled=False, **kwargs)
        self.observed.label = Label(self.observed.id,
                                    kwargs.pop('symptom_name', 'Undefined'))

    symptom_id = IntegerField(widget=widgets.HiddenInput())
    observed = BooleanField()
    details = StringField(validators=[length(max=128)])


class ObservedRiskFactorForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)
        self.observed.label = Label(self.observed.id,
                                    kwargs.pop('risk_factor_name', 'Undefined'))

    risk_factor_id = IntegerField(widget=widgets.HiddenInput())
    observed = RadioField(
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int, )
    details = StringField(validators=[length(max=128)])


class SecondaryRiskFactorForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(
            csrf_enabled=False, **kwargs)
        self.observed.label = Label(self.observed.id,
                                    kwargs.pop('risk_factor_name', 'Undefined'))

    risk_factor_id = IntegerField(widget=widgets.HiddenInput())
    observed = BooleanField()
    details = StringField(validators=[length(max=128)])


FLU_TYPE_CHOICES = (('A', 'A'),
                    ('B', 'B'),
                    ('Inconclusive', 'Inconclusivo'),
                    ('Não Realizado', 'Não Realizado'),
                    ('Ignorado', 'Ignorado')),
FLU_SUBTYPE_CHOICES = (('H1', 'H1'),
                       ('H3', 'H3'),
                       ('Victoria', 'Victoria'),
                       ('Yamagata', 'Yamagata'),
                       ('Não Subtipado', 'Não SubtipADO'),
                       ('Não Subtipável', 'Não SubtipÁVEL'),
                       ('Ignorado', 'Ignorado'))


class CdcExamForm(FlaskForm):
    def __init__(self, **kwargs):
        super(CdcExamForm, self).__init__(csrf_enabled=False, **kwargs)

    flu_type = SelectField(
        'Tipagem',
        choices=FLU_TYPE_CHOICES,
        default='Ignorado',
        coerce=str, )
    flu_subtype = SelectField(
        'Subtipo OU Linhagem',
        choices=FLU_SUBTYPE_CHOICES,
        default='Ignorado',
        coerce=str, )
    dominant_ct = FloatField('CT (principal)', validators=[Optional()])
    details = StringField(
        'Informações adicionais sobre exame', validators=[length(max=128)])


class SampleForm(FlaskForm):
    def __init__(self, **kwargs):
        super(SampleForm, self).__init__(csrf_enabled=False, **kwargs)

    collection_date = DateField(
        'Data de coleta', format='%d/%m/%Y', validators=[InputRequired()])
    semepi = IntegerField(
        'Semana Epidemiológica (Coleta)', validators=[Optional()])
    admission_date = DateField(
        'Data de Entrada no LVRS',
        format='%d/%m/%Y',
        validators=[InputRequired()])
    details = StringField('Informações adicionais')
    method_id = cfields.MethodSelectField()
    cdc_exam = FormField(label='Resultado Exame CDC', form_class=CdcExamForm)


class AdmissionForm(FlaskForm):
    id_lvrs_intern = StringField(
        'Número Interno', validators=[InputRequired()])
    first_symptoms_date = DateField(
        'Data dos Primeiros Sintomas',
        format='%d/%m/%Y',
        validators=[Optional()])
    semepi_symptom = IntegerField(
        'Semana Epidemiológica (Sintomas)', validators=[Optional()])
    state = StringField(label='UF (Estado)',
                        validators=[length(max=2)])
    city = StringField(label='Município de registro do caso',
                       validators=[length(max=128)])
    health_unit = StringField('Unidade de Saúde')
    requesting_institution = StringField('Instituição Solicitante')
    details = StringField('Informações Adicionais')
    patient = FormField(PatientForm, label='Dados do Paciente')
    submit = SubmitField('Criar')
