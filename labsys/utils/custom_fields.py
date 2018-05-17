from wtforms.fields import RadioField


class NullBooleanField(RadioField):
    DEFAULT_CHOICES = ((True, 'Sim'), (False, 'Não'), (None, 'Ignorado'))
    TRUE_VALUES = ('True', 'true')
    FALSE_VALUES = ('False', 'false')
    NONE_VALUES = ('None', 'none', 'null', '')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.choices = kwargs.pop('choices', self.DEFAULT_CHOICES)

    def iter_choices(self):
        for value, label in self.choices:
            yield (value, label, value == self.data)

    def process_data(self, value):
        if value not in (True, False):
            self.data = None
        else:
            self.data = value

    def _parse_str_to_null_bool(self, input_str):
        if input_str in self.TRUE_VALUES:
            return True
        if input_str in self.FALSE_VALUES:
            return False
        if input_str in self.NONE_VALUES:
            return None
        raise ValueError

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self._parse_str_to_null_bool(valuelist[0])
            except ValueError:
                raise ValueError(self.gettext(
                    'Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        for value, _ in self.choices:
            if self.data == value:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))
