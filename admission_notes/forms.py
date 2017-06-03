from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from .models import AdmissionNote

from labsys.settings.base import DATE_INPUT_FORMATS


class AdmissionNoteForm(forms.ModelForm):

    class Meta:
        model = AdmissionNote
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdmissionNoteForm, self).__init__(*args, **kwargs)
        # Builds automacally using default
        #self.helper = FormHelper(self)
        # If you want to manipulate some bits of a big layout,
        # use dynamic layouts (Docs)
        # FormHelper attributes:
        # http://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
        self.helper = FormHelper()
        # self.helper.form_action = 'admission_notes:create'
        #self.helper.form_method = 'post'
        # action set to reverse('<form_action>')
        self.helper.form_tag = False
        self.helper.form_id = 'id-admissionNoteForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class= 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Enviar'))

        self.fields['admission_date'].input_formats = DATE_INPUT_FORMATS
