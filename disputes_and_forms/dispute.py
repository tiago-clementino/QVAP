# -*- coding: utf-8 -*-
class Dispute:

    def __init__(self, id, first, second, third, fourth):
        self.id = id
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth

    def __eq__(self, other):
        """Override the default Equals behavior"""
        other_items = other.get_items()
        return self.first in other_items and self.second in other_items and self.third in other_items and self.fourth in other_items

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        other_items = other.get_items()
        return not self.first in other_items or not self.second in other_items or not self.third in other_items or not self.fourth in other_items


    def get_items(self):
        return [self.first,self.second,self.third,self.fourth]

    @property
    def id(self):
         return self._id

    @id.setter
    def id(self, value):
         self._id = value
