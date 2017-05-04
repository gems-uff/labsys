import datetime #for checking renewal date range.
import collections

#from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms

from betterforms import multiform

from .models import (Patient, AdmissionNote, FluVaccine,
    CollectionType, CollectedSample,
    Symptom, ObservedSymptom,
)


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
    class Meta:
        model = FluVaccine
        fields = [
            'was_applied',
        ]


class AdmissionNoteMultiForm(multiform.MultiModelForm):
    form_classes = {
        'patient_form': PatientForm,
        'admission_note_form': AdmissionNoteForm,
        'flu_vaccine': FluVaccineForm,
    }
