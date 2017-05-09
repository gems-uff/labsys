import datetime #for checking renewal date range.

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import (Patient, AdmissionNote, FluVaccine,
    CollectionType, CollectedSample,
    Symptom, ObservedSymptom,
)

from fiocruz.settings.base import DATE_INPUT_FORMATS


class AdmissionNoteForm(forms.ModelForm):
    class Meta:
        model = AdmissionNote
        fields = [
            'id_gal_origin',
        ]


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name',
        ]


class FluVaccineForm(forms.ModelForm):
    date_applied = forms.DateField(input_formats=DATE_INPUT_FORMATS)

    class Meta:
        model = FluVaccine
        exclude = ['admission_note', ]
