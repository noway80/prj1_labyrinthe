#!/usr/bin/python3
# -*- coding: Utf-8 -*



class Objet:
    """ objet seringe , ether and needle"""

    def __init__(self,nom_image,nom):
        """attribut """
        self.set_position=[0,0]
        self.photo=nom_image
        self.photoimage=""
        self.name=nom
        self.locate=""# objet on zone

    @property
    def position(self):
    	"""returm position x,y in list"""
    	return [self.set_position]
	    
    
class Decor:
    """ decor in zone"""

    def __init__(self,nom_image,nom):
        self.tab_position=[]
        self.photo=nom_image
        self.photoimage=""
        self.name=nom
        self.locate=""# objet on zone
	    
    def add_position(self,pos):
        """ append position """
        self.tab_position.append(pos)
    
    @property
    def position(self):
    	"""return list of positions"""
    	return self.tab_position