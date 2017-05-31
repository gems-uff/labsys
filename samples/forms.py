from django import forms
from django.forms.formsets import BaseFormSet

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

    class Meta:
        model = FluVaccine
        fields = [
            'was_applied',
            'date_applied',
        ]

    def __init__(self, *args, **kwargs):
        super(FluVaccineForm, self).__init__(*args, **kwargs)
        self.fields['date_applied'].input_formats = DATE_INPUT_FORMATS

    def save_fk(self, foreign_key=None):
        # TODO: raise error if foreign_key is None
        flu_vaccine = super().save(commit=False)
        flu_vaccine.admission_note = foreign_key
        flu_vaccine = super().save()
        return flu_vaccine

    # TODO: move it to change method, since it is related to more than one field
    def clean_date_applied(self):
        date_applied = self.cleaned_data['date_applied']
        if self.cleaned_data['was_applied'] and date_applied is None:
            raise forms.ValidationError("Fornecer data de aplicação da vacina")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return date_applied


class CollectedSampleForm(forms.ModelForm):
    other_collection_type = forms.ModelChoiceField(
        label="Outro método de coleta",
        queryset=CollectionType.objects.filter(is_primary=False),
        required=False,
    )

    class Meta:
        model = CollectedSample
        fields = [
            'collection_type',
            'other_collection_type',
            'collection_date',
        ]

    def __init__(self, *args, **kwargs):
        super(CollectedSampleForm, self).__init__(*args, **kwargs)
        self.fields['collection_type'].queryset = \
            CollectionType.objects.filter(is_primary=True)
        self.fields['collection_type'].required = False
        self.fields['collection_date'].input_formats = DATE_INPUT_FORMATS

    def save_fk(self, foreign_key=None):
        # TODO: raise program (not user) error if foreign_key is None
        collected_sample = super().save(commit=False)
        collected_sample.admission_note = foreign_key
        collected_sample = super().save()
        return collected_sample

    def clean(self):
        cleaned_data = super(CollectedSampleForm, self).clean()
        collection_type = cleaned_data.get('collection_type')
        other_collection_type = cleaned_data.get('other_collection_type')

        if collection_type and other_collection_type:
            raise forms.ValidationError(
                "Selecionar somente um método de coleta"
            )

        if collection_type is None and other_collection_type is None:
            raise forms.ValidationError(
                "Selecionar pelo menos um método de coleta"
            )

        if other_collection_type and collection_type is None:
            cleaned_data['collection_type'] = other_collection_type

        return cleaned_data


class BaseCollectedSampleFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that all collected samples have both
        method and collection date.
        """
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                collection_type = form.cleaned_data['collection_type']
                collection_date = form.cleaned_data['collection_date']

                # Check all samples have both date and method
                if collection_type and not collection_date:
                    raise forms.ValidationError(
                        "Todas as amostras devem ter uma data de coleta",
                        code="missing_collection_date",
                    )
                elif collection_date and not collection_type:
                    raise forms.ValidationError(
                        "Todas as amostras devem ter um método de coleta",
                        code="missing_collection_type",
                    )


class ObservedSymptomForm(forms.ModelForm):

    class Meta:
        model = ObservedSymptom
        fields = [
            'symptom',
            'observed',
        ]
        widgets = {
            'symptom': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(ObservedSymptomForm, self).__init__(*args, **kwargs)

    def save_fk(self, foreign_key=None):
        # TODO: raise program (not user) error if foreign_key is None
        observed_symptom = super().save(commit=False)
        observed_symptom.admission_note = foreign_key
        observed_symptom = super().save()
        return observed_symptom

    def clean(self):
        cleaned_data = super(ObservedSymptomForm, self).clean()
        symptom = cleaned_data.get('symptom')

        # TODO: validate

        return cleaned_data


class BaseObservedSymptomFormSet(BaseFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseObservedSymptomFormSet, self).__init__(*args, **kwargs)
        #self.queryset = Symptom.objects.filter(is_primary=True)

    def clean(self):
        if any(self.errors):
            return
