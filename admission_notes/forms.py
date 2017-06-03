from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import AdmissionNote

from labsys.settings.base import DATE_INPUT_FORMATS


class AdmissionNoteForm(forms.ModelForm):

    class Meta:
        model = AdmissionNote
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdmissionNoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'


        self.helper.layout = Layout(
            Fieldset(
                'Dados institucionais',
                'id_gal',
                'admission_date',
                'requester',
                'health_unit',
                'state',
                'city',
            ),
            FormActions(
                Submit('save', 'Salvar'),
                Button('cancel', 'Cancelar'),
            ),
        )

        self.fields['admission_date'].input_formats = DATE_INPUT_FORMATS
