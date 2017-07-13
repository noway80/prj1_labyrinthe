#!/usr/bin/python3
# -*- coding: Utf-8 -*
import threading


class Character:
	
    def __init__(self,nom_image,nom):
        """ int file png and name"""
        self.set_position=[0,0]
        self.photo=nom_image
        self.name=nom
        self.dict_bag={}
        self.univers=""# zone
        self.locate=""

    def move(self,event,a,b):
        """move on zone with x,y"""
        a, b = [sum(x) for x in zip((a, b), self.position[0])]
        if (a, b) not in self.univers.wall.position and a in range(self.univers.width) and b in range(self.univers.width):
            
            self.set_position=[a,b]
            self.univers.draw_entity(self)
            for obj in self.univers.tab_objet:
            	self.objet_in_case(obj) 
            self.end_game()
    
    def objet_in_case(self,objet):
       """ test if character on objet , if true  =>> in the bag"""
       if self.position== objet.position:
       		self.univers.zone_c.delete(objet.locate)
       		self.bag[objet.name]=objet.position
       		self.univers.tab_objet.remove(objet)
       		threading.Thread(None, self.univers.affiche_compteur,None,(self.bag,)).start()

    def end_game(self):
        """ Desactivates commands and displays the result of the game if one is at the end"""
        if self.position == self.univers.guardian.position:
            self.univers.desactiv_command()
            if len(self.bag) == 3:
                self.univers.zone_c.delete(self.univers.guardian.locate)
                texte = "You win !!!!!!"
            else:
                self.univers.zone_c.delete(self.locate)
                texte = "You Lose !!!!!!!!!"
            self.txt = self.univers.zone_c.create_text(int(self.univers.width * self.univers.dimension_sprite / 2), int(
                self.univers.width * self.univers.dimension_sprite / 2), text=texte, font="Arial 16 italic bold", fill="white")

    @property
    def bag(self):
        """return the dict"""
        return self.dict_bag
    
    def add_bag(self,nom,pos):
        """ store objet"""
        self.dict_bag[nom]=pos

    @property# objet on zone
    def position(self):
        """return list position"""
        return [self.set_position]