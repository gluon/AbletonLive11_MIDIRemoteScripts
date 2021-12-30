from novation.novation_base import NovationBase


class CustomNovationBase(NovationBase):
    def __init__(self, *a, **k):
        super(CustomNovationBase, self).__init__(*a, **k)
