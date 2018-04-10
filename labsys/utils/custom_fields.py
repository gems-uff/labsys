from wtforms.fields import RadioField

class NullBooleanField(RadioField):
    def iter_choices(self):
        for value, label in self.choices:
            yield (value, label, value == self.data)

    def process_data(self, value):
        if isinstance(value, bool) is False and value is not None:
            self.data = None
        else:
            self.data = value

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = valuelist[0]
            except ValueError:
                raise ValueError(self.gettext('Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        for value, _ in self.choices:
            if self.data == value:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))
