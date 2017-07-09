from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, FormField, FormField, RadioField, HiddenField,
    FieldList, BooleanField, Label, DateField, SelectField
)
from wtforms.validators import DataRequired, Optional


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PatientForm(FlaskForm):
    name = StringField('Nome do paciente', validators=[DataRequired()])


YES_NO_IGNORED_CHOICES = [(1, 'Sim'), (0, 'Nao'), (9, 'Ignorado')]
class VaccineForm(FlaskForm):
    def __init__(self, **kwargs):
        super(VaccineForm, self).__init__(csrf_enabled=False, **kwargs)

    applied = RadioField(
        label='Aplicada',
        choices=YES_NO_IGNORED_CHOICES,
        default=9,
        coerce=int,
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
        super(SecondarySymptomForm, self).__init__(csrf_enabled=False, **kwargs)
        self.observed.label = Label(
            self.observed.id, kwargs.pop('symptom_name', 'Undefined'))

    symptom_id = HiddenField()
    observed = BooleanField()
    details = StringField()


class CdcForm(FlaskForm):
    def __init__(self, **kwargs):
        super(CdcForm, self).__init__(csrf_enabled=False, **kwargs)


class SampleForm(FlaskForm):
    def __init__(self, **kwargs):
        super(SampleForm, self).__init__(csrf_enabled=False, **kwargs)
        #self.method.choices=kwargs.pop('method_choices', [(0, 'Invalid')])

    collection_date = DateField(
        'Data de coleta',
        format='%d/%m/%Y',
        validators=[Optional()]
    )
    method = SelectField(
        'Método de coleta',
        coerce=int,
        # Pass choices in the view: dynamic, see docs
    )


class AdmissionForm(FlaskForm):
    id_lvrs_intern = StringField('Número interno', validators=[
        DataRequired()])
    patient = FormField(PatientForm)
    vaccine = FormField(VaccineForm)
    symptoms = FieldList(FormField(ObservedSymptomForm))
    sec_symptoms = FieldList(FormField(SecondarySymptomForm))
    samples = FieldList(FormField(SampleForm), min_entries=1)
    submit = SubmitField('Criar')
