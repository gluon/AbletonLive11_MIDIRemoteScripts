from ableton.v2.control_surface.component import Component
from ableton.v2.control_surface.components.session_overview import (
    SessionOverviewComponent,
)


class CustomSessionOverviewComponent(SessionOverviewComponent):
    def __init__(self, *a, **k):
        super(CustomSessionOverviewComponent, self).__init__(*a, **k)
