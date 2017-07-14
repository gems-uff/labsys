from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, FormField, FormField, RadioField, HiddenField,
    FieldList, BooleanField, Label, DateField, SelectField, IntegerField
)
from wtforms.validators import InputRequired, Optional


class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[InputRequired()])
    submit = SubmitField('Enviar')


class PatientForm(FlaskForm):
    name = StringField('Nome do paciente', validators=[InputRequired()])
    birth_date = DateField('Data de nascimento', format='%d/%m/%Y')
    age = IntegerField('Idade', validators=[Optional()])
    age_unit = RadioField(
        label='Tipo idade',
        choices=((1, 'Anos'), (2, 'Meses'), (3, 'Dias'), (4, 'Horas')),
        default=1,
        coerce=int,
    )
    gender = RadioField(
        label='Sexo',
        choices=((1, 'Masculino'), (2, 'Feminino'), (9, 'Ignorado')),
        default=9,
        coerce=int,
    )
    country = SelectField(
        label='País de residência',
        choices=((1, 'Brasil'), (2, 'Argentina'), (3, 'Outro')),
        default=1,
        coerce=int,
    )
    state = SelectField(
        label='UF (Estado)',
        choices=((1, 'RJ'), (2, 'ES'), (3, 'Outro')),
        default=3,
        coerce=int,
    )
    city = SelectField(
        label='Cidade',
        choices=((1, 'Rio de Janeiro'), (2, 'Niterói'), (3, 'Outra')),
        default=3,
        coerce=int,
    )
    neighborhood = StringField('Bairro', validators=[Optional()])
    # TODO: change to RadioField =)
    zone = SelectField(
        label='Zona',
        choices=((1, 'Urbana'), (2, 'Rural'), (3, 'Periurbana'),
                 (4, 'Ignorado')),
        default=4,
        coerce=int,
    )




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


class SymptomForm(FlaskForm):
    name = StringField('Sintoma')
    primary = BooleanField('Primario?')
    submit = SubmitField('Criar')


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

    details = StringField('Info adicional')


class SampleForm(FlaskForm):
    def __init__(self, **kwargs):
        super(SampleForm, self).__init__(csrf_enabled=False, **kwargs)
        #self.method.choices=kwargs.pop('method_choices', [(0, 'Invalid')])

    collection_date = DateField(
        'Data de coleta',
        format='%d/%m/%Y',
        validators=[InputRequired()]
    )
    method = SelectField(
        'Método de coleta',
        coerce=int,
        # Pass choices in the view: dynamic, see docs
    )
    cdc_exam = FormField(CdcForm)


class AdmissionForm(FlaskForm):
    id_lvrs_intern = StringField('Número interno',
                                 validators=[InputRequired()])
    patient = FormField(PatientForm)
    vaccine = FormField(VaccineForm)
    hospitalization = FormField(HospitalizationForm)
    uti_hospitalization = FormField(UTIHospitalizationForm)
    clinical_evolution = FormField(ClinicalEvolutionForm)
    symptoms = FieldList(FormField(ObservedSymptomForm))
    sec_symptoms = FieldList(FormField(SecondarySymptomForm))
    samples = FieldList(FormField(SampleForm), min_entries=1)
    submit = SubmitField('Criar')