
from Kernel.Db import schema

class Input(object):
    def __init__(self, message):
        self.message = message

class PointInput(Input):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, schema.Point):
            pass
        self._value = value


class LengthInput(Input):
    pass
