from django import forms
from django.utils.safestring import mark_safe


class YesNoIgnoredField(forms.NullBooleanField):
    widget = forms.widgets.RadioSelect(
        attrs={'class': 'inline'},
        choices=(
            (True, "Sim"), (False, "Não"), (None, "Ignorado"),
        ),
    )

