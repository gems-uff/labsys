from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button
from crispy_forms.bootstrap import FormActions

from labsys.settings.base import DATE_INPUT_FORMATS
from .models import CollectionMethod, CollectedSample


class CollectedSampleForm(forms.ModelForm):
    other_collection_method = forms.ModelChoiceField(
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
            'details',
        ]

    def __init__(self, *args, **kwargs):
        super(CollectedSampleForm, self).__init__(*args, **kwargs)
        self.fields['collection_method'].queryset = \
            CollectionMethod.objects.filter(is_primary=True)
        self.fields['collection_method'].required = False
        self.fields['collection_date'].input_formats = DATE_INPUT_FORMATS

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'

        self.helper.layout = Layout(
            Fieldset(
                'Amostra',
                'collection_method',
                'other_collection_method',
                'collection_date',
                'details',
            ),
        )

    def save(self, admin_note=None, commit=True):
        self.instance.admission_note = admin_note
        super(CollectedSampleForm, self).save(commit)
        return self.instance

    def clean(self):
        cleaned_data = super(CollectedSampleForm, self).clean()
        collection_method = cleaned_data.get('collection_method')
        other_collection_method = cleaned_data.get('other_collection_method')

        if collection_method and other_collection_method:
            raise forms.ValidationError(
                "Selecionar somente um método de coleta"
            )

        if collection_method is None and other_collection_method is None:
            raise forms.ValidationError(
                "Selecionar pelo menos um método de coleta"
            )

        if other_collection_method and collection_method is None:
            cleaned_data['collection_method'] = other_collection_method

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
                collection_method = form.cleaned_data['collection_method']
                collection_date = form.cleaned_data['collection_date']

                # Check all samples have both date and method
                if collection_method and not collection_date:
                    raise forms.ValidationError(
                        "Todas as amostras devem ter uma data de coleta",
                        code="missing_collection_date",
                    )
                elif collection_date and not collection_method:
                    raise forms.ValidationError(
                        "Todas as amostras devem ter um método de coleta",
                        code="missing_collection_method",
                    )


CollectedSampleFormSet = formset_factory(
    CollectedSampleForm,
    # formset=BaseCollectedSampleFormSet,
    extra=2,
)