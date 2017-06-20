from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.bootstrap import FormActions

from .models import (
    AdmissionNote,
    ISimpleDatedEvent,
    FluVaccine,
    ClinicalEvolution,
    Hospitalization,
    UTIHospitalization,
)

from labsys.settings.base import DATE_INPUT_FORMATS


class AdmissionNoteForm(forms.ModelForm):

    class Meta:
        model = AdmissionNote
        # fields = '__all__'
        exclude = ['patient']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(AdmissionNoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'


        self.helper.layout = Layout(
            Fieldset(
                'Dados institucionais',
                'id_request_gal',
                'id_lvrs_intern',
                'admission_date',
                'requester',
                'health_unit',
                'state',
                'city',
                'details',
            ),
        )

        self.fields['admission_date'].input_formats = DATE_INPUT_FORMATS

    def save(self, patient=None, commit=True):
        if patient is not None:
            self.instance.patient = patient
        super(AdmissionNoteForm, self).save(commit)
        return self.instance


class ISimpleDatedEventForm(forms.ModelForm):

    class Meta:
        model = ISimpleDatedEvent
        exclude = ['admission_note']

    def __init__(self, *args, **kwargs):
        super(ISimpleDatedEventForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = DATE_INPUT_FORMATS
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'

    def save(self, admin_note=None, commit=True):
        if admin_note is not None:
            self.instance.admission_note = admin_note
        super(ISimpleDatedEventForm, self).save(commit)
        return self.instance


class FluVaccineForm(ISimpleDatedEventForm):

    class Meta:
        model = FluVaccine
        exclude = ['admission_note']

    def __init__(self, *args, **kwargs):
        super(FluVaccineForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Tomou vacina contra a gripe?',
                'occurred',
                'date',
            ),
        )
        self.fields['occurred'].label = 'Foi vacinado'
        self.fields['occurred'].help_text = 'Vacinado nos últimos 12 meses'
        self.fields['date'].label = 'Data de vacinação'


class ClinicalEvolutionForm(ISimpleDatedEventForm):

    class Meta:
        model = ClinicalEvolution
        exclude = ['admission_note']

    def __init__(self, *args, **kwargs):
        super(ClinicalEvolutionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Evoluiu para óbito?',
                'occurred',
                'date',
            ),
        )
        self.fields['occurred'].label = 'Óbito'
        self.fields['date'].label = 'Data de óbito'


class HospitalizationForm(ISimpleDatedEventForm):

    class Meta:
        model = Hospitalization
        exclude = ['admission_note']

    def __init__(self, *args, **kwargs):
        super(HospitalizationForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Ocorreu internação (hospital)?',
                'occurred',
                'date',
            ),
        )
        self.fields['occurred'].label = 'Internado hospital'
        self.fields['date'].label = 'Data de internação'


class UTIHospitalizationForm(ISimpleDatedEventForm):

    class Meta:
        model = UTIHospitalization
        exclude = ['admission_note']

    def __init__(self, *args, **kwargs):
        super(UTIHospitalizationForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Foi internado em UTI?',
                'occurred',
                'date',
            ),
        )
        self.fields['occurred'].label = 'Internado UTI'
        self.fields['date'].label = 'Data de internação'

