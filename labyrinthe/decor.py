#!/usr/bin/python3
# -*- coding: Utf-8 -*
from labyrinthe.entity import *

class Decor(Objet):
    """ decor in zone"""

    def __init__(self,nom_image,nom):
        Objet.__init__(self, nom_image,nom)
        #super().__init__()
        self.tab_position=[]
        
    def add_position(self,pos):
        """ append position """
        self.tab_position.append(pos)
    
    @property
    def position(self):
    	"""return list of positions"""
    	return self.tab_position