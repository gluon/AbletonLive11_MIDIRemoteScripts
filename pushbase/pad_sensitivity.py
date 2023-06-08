from __future__ import absolute_import, print_function, unicode_literals
from builtins import zip
from itertools import repeat
from ableton.v2.base import find_if, nop, second, task
from ableton.v2.control_surface import Component

class PadUpdateComponent(Component):

    def __init__(self, all_pads=tuple(), parameter_sender=nop, default_profile=None, update_delay=0, *a, **k):
        (super(PadUpdateComponent, self).__init__)(*a, **k)
        self.parameter_sender = parameter_sender
        self._all_pads = set(all_pads)
        self._modified_pads = set(all_pads)
        self._profiles = {'default': default_profile}
        self._profile_for = dict(list(zip(all_pads, repeat('default'))))
        self._profile_count = {'default': len(all_pads)}
        self._update_task = self._tasks.add(task.sequence(task.wait(update_delay), task.run(self._update_modified)))
        self._update_task.restart()

    def set_profile(self, profile_id, parameters):
        self._profiles[profile_id] = parameters
        self._profile_count.setdefault(profile_id, 0)
        affected = [k for k, v in self._profile_for.items() if v == profile_id]
        self._add_modified_pads(affected)

    def get_profile(self, profile_id):
        return self._profiles[profile_id]

    def set_pad(self, pad, new_profile):
        old_profile = self._profile_for[pad]
        if old_profile != new_profile:
            self._add_modified_pads([pad])
            self._profile_for[pad] = new_profile
            self._profile_count[old_profile] -= 1
            self._profile_count[new_profile] += 1

    def update(self):
        super(PadUpdateComponent, self).update()
        self._add_modified_pads(self._all_pads)
        self._update_modified()

    def _update_modified(self):
        if self.is_enabled():
            if self._modified_pads:
                largest_profile, largest_count = max((iter(self._profile_count.items())),
                  key=second)
                if len(self._all_pads) - largest_count + 1 < len(self._modified_pads):
                    self.parameter_sender(self._profiles[largest_profile])
                    for pad in self._all_pads:
                        profile = self._profile_for[pad]
                        if profile != largest_profile:
                            self.parameter_sender(self._profiles[profile], pad)

                else:
                    for pad in self._modified_pads:
                        self.parameter_sender(self._profiles[self._profile_for[pad]], pad)

                self._modified_pads.clear()
        self._update_task.kill()

    def _add_modified_pads(self, pads):
        self._modified_pads.update(pads)
        self._update_task.restart()