from __future__ import absolute_import, print_function, unicode_literals
from dataclasses import dataclass
from ...base import BooleanContext

@dataclass
class Content:
    value: object

    def __eq__(self, other):
        if isinstance(other, Content):
            return self.value == other.value
        return self.value == other

    @staticmethod
    def from_object(obj):
        if isinstance(obj, Content):
            return obj
        return Content(obj)


updating_display = BooleanContext()