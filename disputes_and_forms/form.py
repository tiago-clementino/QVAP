# -*- coding: utf-8 -*-


class Form:

    _dispute = []
    def __init__(self, id):
        self._id = id

    def append_dispute(self, dispute):
        self._dispute.append(dispute)

    def audict_dispute(self, dispute, dispute_position):
        pass
