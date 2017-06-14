from django import forms
from django.forms import formset_factory, BaseInlineFormSet

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button

from .models import Symptom, ObservedSymptom


class ObservedSymptomInlineFormset(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(ObservedSymptomInlineFormset, self).__init__(*args, **kwargs)
        #self.initial = Symptom.get_primary_symptoms_dict()


class SecondarySymptomsForm(forms.Form):

    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.filter(is_primary=False),
        widget = forms.CheckboxSelectMultiple(),
        required=False,
    )
    details = forms.CharField(max_length=255, required=False)


    def __init__(self, *args, **kwargs):
        super(SecondarySymptomsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.field_class = 'col-lg-4'

        self.helper.layout = Layout(
            Fieldset(
                'Sintomas secundários',
                'symptoms',
                'details',
            ),
        )


class ObservedSymptomForm(forms.ModelForm):

    class Meta:
        model = ObservedSymptom
        fields = [
            'symptom',
            'observed',
            'details',
        ]
        widgets = {
            'details': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
        }


    def __init__(self, *args, **kwargs):
        super(ObservedSymptomForm, self).__init__(*args, **kwargs)
        # TODO: receive symptom key in args


ObservedSymptomFormSet = formset_factory(
    ObservedSymptomForm,
    extra=0,
)