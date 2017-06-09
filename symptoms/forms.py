from django import forms

from labsys.custom.forms import YesNoIgnoredField
from .models import ObservedSymptom


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
