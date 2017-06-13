from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import AdmissionNote

from labsys.settings.base import DATE_INPUT_FORMATS


class AdmissionNoteForm(forms.ModelForm):

    class Meta:
        model = AdmissionNote
        # fields = '__all__'
        exclude = ['patient']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(AdmissionNoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'


        self.helper.layout = Layout(
            Fieldset(
                'Dados institucionais',
                'id_request_gal',
                'id_lvrs_intern',
                'admission_date',
                'requester',
                'health_unit',
                'state',
                'city',
                'details',
            ),
        )

        self.fields['admission_date'].input_formats = DATE_INPUT_FORMATS
