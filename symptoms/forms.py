from django import forms
from django.forms import formset_factory, BaseInlineFormSet

from .models import Symptom, ObservedSymptom


class ObservedSymptomInlineFormset(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(ObservedSymptomInlineFormset, self).__init__(*args, **kwargs)
        #self.initial = Symptom.get_primary_symptoms_dict()


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