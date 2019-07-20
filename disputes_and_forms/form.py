# -*- coding: utf-8 -*-


class Form:

    _disputes = []
    def __init__(self, id):
        self._id = id

    def append_dispute(self, dispute):
        self._disputes.append(dispute)

    def audict_dispute(self, dispute, dispute_position):
        first = 0#counts the ocorrences of the first item in other disputes in form (and so forth)
        second = 0
        third = 0
        fourth = 0
        for my_dispute in self._disputes:
            dispute_items = my_dispute.get_items()
            if dispute.first in dispute_items:
                first = first + 1
            if dispute.second in dispute_items:
                second = second + 1
            if dispute.third in dispute_items:
                third = third + 1
            if dispute.fourth in dispute_items:
                fourth = fourth + 1
        result = first >= 3 or second >= 3 or third >= 3 or fourth >= 3#3 is the maximum of items as a criteron to avoid bias
        if Len(self._disputes) > dispute_position + 1:
            dispute_items = self._disputes[dispute_position - 1].get_items()
            return result and not (
              dispute.first in dispute_items or
              dispute.second in dispute_items or
              dispute.third in dispute_items or 
              dispute.fourth in dispute_items
            ):
        else:
            return result
