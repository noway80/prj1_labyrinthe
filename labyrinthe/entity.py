#!/usr/bin/python3
# -*- coding: Utf-8 -*


class Objet:
    """ objet seringe , ether and needle"""

    def __init__(self, nom_image, nom):
        """attribut """
        self.set_position = [0, 0]
        self.photo = nom_image
        self.photoimage = ""
        self.name = nom
        self.locate = ""  # objet on zone

    @property
    def position(self):
        """returm position x,y in list"""
        return [self.set_position]

    def __str__(self):
        return self.name
