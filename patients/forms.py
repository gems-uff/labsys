from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import Patient, Locality

from labsys.settings.base import DATE_INPUT_FORMATS


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'


        self.helper.layout = Layout(
            Fieldset(
                'Dados do paciente',
                'name',
                'birth_date',
                'age_in_hours',
                'gender',
                'pregnant',
                'residence',
            ),
        )

        self.fields['admission_date'].input_formats = DATE_INPUT_FORMATS
