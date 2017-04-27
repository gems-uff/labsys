from django import forms


class YesNoIgnoredField(forms.NullBooleanField):
    widget = forms.widgets.RadioSelect(
        choices=(
            (True, "Sim"), (False, "Não"), (None, "Ignorado"),
        ),
    )
