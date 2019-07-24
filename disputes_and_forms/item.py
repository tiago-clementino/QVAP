# -*- coding: utf-8 -*-
class Item:

    def __init__(self, id, GDrive_URL, copy, shape, material, surface, color, constitution):
        self.id = id
        self.GDrive_URL = GDrive_URL
        self.copy = copy
        self.shape = shape
        self.material = material
        self.surface = surface
        self.color = color
        self.constitution = constitution

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.id == other.id

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        return self.id != other.id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def dispute(self):
        return self._dispute

    @dispute.setter
    def dispute(self, value):
        self._dispute = value

    def __str__(self):
        return str(self.id)

    @property
    def GDrive_URL(self):
        return self._GDrive_URL

    @GDrive_URL.setter
    def GDrive_URL(self, value):
        self._GDrive_link = value
        self._GDrive_ID = value.replace("https://drive.google.com/open?id=", "")
        self._GDrive_URL = "https://drive.google.com/uc?export=view&id="+self._GDrive_ID
