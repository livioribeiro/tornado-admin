from abc import ABCMeta, abstractmethod
from enum import Enum, unique


class FormField(metaclass=ABCMeta):
    pass


class InputFormField(FormField, metaclass=ABCMeta):
    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError()


class TextInput(InputFormField):
    @property
    def type(self):
        return 'text'


class PasswordInput(InputFormField):
    @property
    def type(self):
        return 'password'


class NumberInput(InputFormField):
    @property
    def type(self):
        return 'number'


class FileInput(InputFormField):
    @property
    def type(self):
        return 'file'


class Textarea(FormField):
    def __init__(self, rows=4, cols=32):
        self.rows = rows
        self.cols = cols


class ChoiceField(FormField, metaclass=ABCMeta):
    def __init__(self, choices):
        self.choices = choices


@unique
class SingleChoiceType(Enum):
    RADIO = 'RADIO'
    SELECT = 'SELECT'


@unique
class MultiChoiceType(Enum):
    CHECKBOX = 'CHECKBOX'
    SELECT = 'SELECT'


class SingleChoiceField(ChoiceField):
    def __init__(self, field_type: SingleChoiceType, choices=list):
        super().__init__(choices=choices)
        self.field_type = field_type


class MultiChoiceField(ChoiceField):
    def __init__(self, field_type: MultiChoiceType, choices=list):
        super().__init__(choices=choices)
        self.field_type = field_type
