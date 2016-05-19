from abc import ABCMeta, abstractmethod
from enum import Enum, unique


@unique
class InputType(Enum):
    BUTTON = 'button'
    CHECKBOX = 'checkbox'
    COLOR = 'color'
    DATE = 'date'
    DATETIME = 'datetime'
    DATETIME_LOCAL = 'datetime-local'
    EMAIL = 'email'
    FILE = 'file'
    HIDDEN = 'hidden'
    IMAGE = 'image'
    MONTH = 'month'
    NUMBER = 'number'
    PASSWORD = 'password'
    RADIO = 'radio'
    RANGE = 'range'
    RESET = 'reset'
    SEARCH = 'search'
    SUBMIT = 'submit'
    TEL = 'tel'
    TEXT = 'text'
    TIME = 'time'
    URL = 'url'
    WEEK = 'week'


class FormField(metaclass=ABCMeta):
    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.value = None


class InputField(FormField):
    def __init__(self, name, label, ftype: InputType=InputType.TEXT):
        super().__init__(name, label)
        self.type = ftype


class Textarea(FormField):
    def __init__(self, name, label, rows=4, cols=32):
        super().__init__(name, label)
        self.rows = rows
        self.cols = cols


@unique
class SingleChoiceType(Enum):
    RADIO = InputType.RADIO
    SELECT = 'select'


@unique
class MultiChoiceType(Enum):
    CHECKBOX = InputType.CHECKBOX
    SELECT = 'select'


class ChoiceField(FormField, metaclass=ABCMeta):
    def __init__(self, name, label, choices):
        super().__init__(name, label)
        self.choices = choices
        self.type = None

    @abstractmethod
    def has_value(self, value):
        raise NotImplementedError()

    @property
    def is_multiple(self):
        return isinstance(self, MultiChoiceField)

    @property
    def is_input(self):
        return self.type in (SingleChoiceType.RADIO, MultiChoiceType.CHECKBOX)


class SingleChoiceField(ChoiceField):
    def __init__(self, name, label, ftype: SingleChoiceType, choices=list):
        super().__init__(name, label, choices=choices)
        self.type = ftype
        self.value = list()

    def has_value(self, value):
        return value == self.value


class MultiChoiceField(ChoiceField):
    def __init__(self, name, label, ftype: MultiChoiceType, choices=list):
        super().__init__(name, label, choices=choices)
        self.type = ftype
        self.values = list()

    def has_value(self, value):
        return value in self.values

    def _set_value(self, value):
        self.values = value

    value = property(fset=_set_value)
