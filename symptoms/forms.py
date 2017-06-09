from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Div
from crispy_forms.bootstrap import InlineRadios

from labsys.settings.base import DATE_INPUT_FORMATS
from .models import ObservedSymptom


class ObservedSymptomFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ObservedSymptomFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_show_labels = False


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
        # TODO: receive symptom key in args
        # self.helper = ObservedSymptomFormSetHelper()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-2'

'''
        self.helper.layout = Layout(
            'symptom',
            'observed',
            'details',
        )
'''