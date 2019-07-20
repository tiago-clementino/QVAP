# -*- coding: utf-8 -*-


class Dispute:

    def __init__(self, id, first, second, third, fourth):
        self._id = id
        self.first = first
        self.second = second
        self.third = third
        self.fourth = forth

    def get_items(self):
        return [self.first,self.second,self.third,self.fourth]
