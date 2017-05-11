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
    # TODO: see if it's possible not to override "blank=True"
    # when declaring a field
    date_applied = forms.DateField(input_formats=DATE_INPUT_FORMATS,
                                   required=False)

    class Meta:
        model = FluVaccine
        fields = ['was_applied', 'date_applied', ]

    def save_fk(self, foreign_key=None):
        # TODO: raise error if foreign_key is None
        flu_vaccine = super().save(commit=False)
        flu_vaccine.admission_note = foreign_key
        flu_vaccine = super().save()
        return flu_vaccine

    def clean_date_applied(self):
        date_applied = self.cleaned_data['date_applied']
        if self.cleaned_data['was_applied'] and date_applied is None:
            raise forms.ValidationError("Fornecer data de aplicação da vacina")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return date_applied


class CollectedSampleForm(forms.ModelForm):
    collection_date = forms.DateField(input_formats=DATE_INPUT_FORMATS,
                                      required=False)
    other_collection_types = forms.ModelChoiceField(
        queryset=CollectionType.objects.filter(is_primary=False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CollectedSampleForm, self).__init__(*args, **kwargs)
        self.fields['collection_type'].queryset = \
            CollectionType.objects.filter(is_primary=True)

    class Meta:
        model = CollectedSample
        fields = [
            'collection_type',
            'other_collection_types',
            'collection_date',
         ]
