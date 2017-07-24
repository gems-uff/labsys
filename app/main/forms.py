from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, FormField, FormField, RadioField, HiddenField,
    FieldList, BooleanField, Label, DateField, SelectField, IntegerField,
    FloatField,
)
from wtforms.validators import InputRequired, Optional

import app.custom_fields as cfields
import app.models as models


class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[InputRequired()])
    submit = SubmitField('Enviar')


class ResidenceForm(FlaskForm):

    class Meta:
        csrf = False

    country_id = cfields.CountrySelectField(label='País de residência')
    state_id = cfields.StateSelectField(label='UF (Estado)')
    city_id = cfields.CitySelectField(label='Município')
    neighborhood = StringField('Bairro')
    zone = RadioField(
        label='Zona',
        choices=(
            (1, 'Urbana'), (2, 'Rural'), (3, 'Periurbana'), (9, 'Ignorado')),
        default=9,
        coerce=int,
    )
    details = StringField('Detalhes da residência')


class PatientForm(FlaskForm):
    name = StringField('Nome do paciente')
    birth_date = DateField('Data de nascimento', format='%d/%m/%Y',
                           validators=[Optional()])
    age = IntegerField('Idade', validators=[Optional()])
    age_unit = RadioField(
        label='Tipo idade',
        choices=(('Y', 'Anos'), ('M', 'Meses'), ('D', 'Dias'), ('H', 'Horas')),
        default='Y',
        coerce=str,
    )
    gender = RadioField(
        label='Sexo',
        choices=(('M', 'Masculino'), ('F', 'Feminino'), ('I', 'Ignorado')),
        default='I',
        coerce=str,
    )
    residence = FormField(ResidenceForm, label='Residência')


YES_NO_IGNORED_CHOICES = [(1, 'Sim'), (0, 'Nao'), (9, 'Ignorado')]
class DatedEventForm(FlaskForm):

    class Meta:
        csrf = False

    def __init__(self, **kwargs):
        super(DatedEventForm, self).__init__(**kwargs)
        self.occurred.label.text = kwargs.pop('occurred_label', 'Ocorreu')
        self.date.label.text = kwargs.pop('date_label', 'Data')

    occurred = RadioField(
        label='Ocorreu',
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int,
    )
    date = DateField(
        label='Data',
        format='%d/%m/%Y',
        validators=[Optional()]
    )


class VaccineForm(DatedEventForm):
    def __init__(self, **kwargs):
        super(VaccineForm, self).__init__(
            occurred_label='Aplicada',
            date_label='Data da última dose',
            prefix='vaccine',
        )


class HospitalizationForm(DatedEventForm):
    def __init__(self, **kwargs):
        super(HospitalizationForm, self).__init__(
            prefix='hospitalization',
        )


class UTIHospitalizationForm(DatedEventForm):
    def __init__(self, **kwargs):
        super(UTIHospitalizationForm, self).__init__(
            prefix='uti_hospitalization',
        )


class ClinicalEvolutionForm(DatedEventForm):
    def __init__(self, **kwargs):
        super(ClinicalEvolutionForm, self).__init__(
            occurred_label='Evoluiu para óbito',
            prefix='clinical_evolution',
        )


class ObservedSymptomForm(FlaskForm):
    def __init__(self, **kwargs):
        super(ObservedSymptomForm, self).__init__(csrf_enabled=False, **kwargs)
        self.observed.label = Label(
            self.observed.id, kwargs.pop('symptom_name', 'Undefined'))

    symptom_id = HiddenField()
    observed = RadioField(
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int,
    )
    details = StringField()


class SecondarySymptomForm(FlaskForm):
    def __init__(self, **kwargs):
        super(SecondarySymptomForm, self).__init__(
            csrf_enabled=False, **kwargs)
        self.observed.label = Label(
            self.observed.id, kwargs.pop('symptom_name', 'Undefined'))

    symptom_id = HiddenField()
    observed = BooleanField()
    details = StringField()


class CdcForm(FlaskForm):
    def __init__(self, **kwargs):
        super(CdcForm, self).__init__(csrf_enabled=False, **kwargs)

    flu_type = SelectField(
        'Tipagem',
        # TODO: model flu/subtype
        choices=(('A', 'A'), ('B', 'B'),
                 ('Inconclusive', 'Inconclusivo'),
                 ('Não Realizado', 'Não Realizado'),
                 ('Ignorado', 'Ignorado')),
        default='Ignorado',
        coerce=str,
    )
    flu_subtype = SelectField(
        'Subtipo OU Linhagem',
        choices=(('H1', 'H1'), ('H3', 'H3'),
                 ('Victoria', 'Victoria'), ('Yamagata', 'Yamagata'),
                 ('Não Subtipado', 'Não SubtipADO'),
                 ('Não Subtipável', 'Não SubtipÁVEL'),
                 ('Ignorado', 'Ignorado')),
        default='Ignorado',
        coerce=str,
    )
    dominant_ct = FloatField('CT (principal)', validators=[Optional()])
    details = StringField('Informações adicionais')


class SampleForm(FlaskForm):
    def __init__(self, **kwargs):
        super(SampleForm, self).__init__(csrf_enabled=False, **kwargs)

    collection_date = DateField(
        'Data de coleta',
        format='%d/%m/%Y',
        validators=[InputRequired()]
    )
    semepi = IntegerField('Semana Epidemiológica (Coleta)',
                          validators=[Optional()])
    admission_date = DateField(
        'Data de Entrada no LVRS',
        format='%d/%m/%Y',
        validators=[InputRequired()]
    )
    method = cfields.MethodSelectField()
    cdc_exam = FormField(label='Resultado Exame CDC', form_class=CdcForm)


class AdmissionForm(FlaskForm):
    id_lvrs_intern = StringField('Número Interno',
                                 validators=[InputRequired()])
    first_symptoms_date = DateField('Data dos Primeiros Sintomas',
                                    format='%d/%m/%Y',
                                    validators=[Optional()])
    semepi_symptom = IntegerField('Semana Epidemiológica (Sintomas)',
                                  validators=[Optional()])
    state_id = cfields.StateSelectField('UF de Registro do Caso')
    city_id = cfields.CitySelectField('Município de registro do caso')
    health_unit = StringField('Unidade de Saúde')
    requesting_institution = StringField('Instituição Solicitante')
    details = StringField('Informações Adicionais')
    patient = FormField(PatientForm, label='Dados do Paciente')
    vaccine = FormField(VaccineForm, label='Vacina contra Gripe')
    hospitalization = FormField(HospitalizationForm,
                                label='Internação Hospitalar')
    uti_hospitalization = FormField(UTIHospitalizationForm,
                                    label='Internação UTI')
    clinical_evolution = FormField(ClinicalEvolutionForm,
                                   label='Evolução Clínica')
    symptoms = FieldList(FormField(ObservedSymptomForm))
    sec_symptoms = FieldList(FormField(SecondarySymptomForm),
                             label='Sintomas Secundários')
    # TODO: #1 must be dynamic
    samples = FieldList(FormField(label='Amostra', form_class=SampleForm),
                        label='Amostras',
                        min_entries=1)
    submit = SubmitField('Criar')
