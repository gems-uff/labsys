from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button

from labsys.settings.base import DATE_INPUT_FORMATS
from .models import ObservedSymptom


class ObservedSymptomForm(forms.ModelForm):

    class Meta:
        model = ObservedSymptom
        fields = [
            'symptom',
            'observed',
            'details',
        ]

    def __init__(self, *args, **kwargs):
        super(ObservedSymptomForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'

        self.helper.layout = Layout(
            Fieldset(
                'Sintoma',
                'symptom',
                'observed',
                'details',
            ),
        )
