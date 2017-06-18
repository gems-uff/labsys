from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button
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
        self.instance.patient = patient
        super(AdmissionNoteForm, self).save(commit)
        return self.instance

# region ISimpleDatedEvent Forms (should be inherited)
# TODO: check how to do inheritance
class FluVaccineForm(forms.ModelForm):

    class Meta:
        model = FluVaccine
        exclude = ['admission_note']

    def __init__(self, *args, **kwargs):
        super(FluVaccineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'

        self.helper.layout = Layout(
            Fieldset(
                'Tomou vacina contra a gripe?',
                'occurred',
                'date',
            ),
        )
        self.fields['date'].input_formats = DATE_INPUT_FORMATS

    def save(self, admin_note=None, commit=True):
        self.instance.admission_note = admin_note
        super(FluVaccineForm, self).save(commit)
        return self.instance


class ClinicalEvolutionForm(FluVaccineForm):

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


class HospitalizationForm(FluVaccineForm):

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


class UTIHospitalizationForm(FluVaccineForm):

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

