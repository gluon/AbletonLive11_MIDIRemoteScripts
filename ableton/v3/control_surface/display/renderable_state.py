from __future__ import absolute_import, print_function, unicode_literals
from dataclasses import dataclass
from pprint import pformat
from typing import Callable

@dataclass
class StateFilters:
    key_filter = lambda k: not k.startswith('_')
    key_filter: Callable
    value_filter = lambda v: v is not None and v != ''
    value_filter: Callable


class RenderableState:
    repr_filters = StateFilters()

    def __repr__(self):
        return pformat((self.get_repr_data()), indent=4)

    def get_repr_data(self):
        dct = dict(vars(self))
        keys_to_remove = set()
        for key, value in dct.items():
            if not self.repr_filters.key_filter(key):
                keys_to_remove.add(key)
            else:
                if isinstance(value, RenderableState):
                    dct[key] = dct[key].get_repr_data()
            if not self.repr_filters.value_filter(value):
                keys_to_remove.add(key)

        for key in keys_to_remove:
            del dct[key]

        return dct

    @staticmethod
    def from_dict(instance: dict):
        state = RenderableState()
        for key, value in instance.items():
            setattr(state, key, RenderableState.from_dict(value) if isinstance(value, dict) else value)

        return state