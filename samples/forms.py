import datetime #for checking renewal date range.

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import (Patient, AdmissionNote, FluVaccine,
    CollectionType, CollectedSample,
    Symptom, ObservedSymptom,
)

from labsys.settings.base import DATE_INPUT_FORMATS


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
    # TODO: see if it's possible not to override "blank=True" when declaring a field
    date_applied = forms.DateField(input_formats=DATE_INPUT_FORMATS,
                                   required=False)

    class Meta:
        model = FluVaccine
        fields = ['was_applied', 'date_applied', ]

    def save(self, foreign_key=None):
        # TODO: raise error if foreign_key is None
        flu_vaccine = super().save(commit=False)
        flu_vaccine.admission_note = foreign_key
        flu_vaccine = super().save()
        return flu_vaccine

    # TODO: clean_date_applied to check if was_applied is True or False
