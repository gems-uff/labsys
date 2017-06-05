from django.db import models

from samples.custom import forms as cforms


class YesNoIgnoredField(models.NullBooleanField):
    def formfield(self, **kwargs):
        defaults = {'form_class': cforms.YesNoIgnoredField}
        defaults.update(kwargs)
        return super(YesNoIgnoredField, self).formfield(**defaults)
