from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

from labsys.settings.base import DATE_INPUT_FORMATS
from .models import CollectionMethod, CollectedSample


class CollectedSampleForm(forms.ModelForm):
    other_collection_type = forms.ModelChoiceField(
        label="Outro método de coleta",
        queryset=CollectionMethod.objects.filter(is_primary=False),
        required=False,
    )

    class Meta:
        model = CollectedSample
        fields = [
            'collection_method',
            'other_collection_method',
            'collection_date',
        ]

    def __init__(self, *args, **kwargs):
        super(CollectedSampleForm, self).__init__(*args, **kwargs)
        self.fields['collection_type'].queryset = \
            CollectionMethod.objects.filter(is_primary=True)
        self.fields['collection_method'].required = False
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


CollectedSampleFormSet = formset_factory(
    CollectedSampleForm,
    formset=BaseCollectedSampleFormSet
)