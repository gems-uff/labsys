from django import forms


class YesNoIgnoredField(forms.NullBooleanField):
    widget = forms.widgets.RadioSelect(
        attrs={'class': 'inline'},
        choices=(
            (True, "Sim"), (False, "Não"), (None, "Ignorado"),
        ),
    )
