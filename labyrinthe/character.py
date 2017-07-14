#!/usr/bin/python3
# -*- coding: Utf-8 -*
import threading
from labyrinthe.entity import *
import time


class Character(Objet):

    def __init__(self, nom_image, nom):
        """ int file png and name"""
        Objet.__init__(self, nom_image, nom)
        self.dict_bag = {}
        self.univers = ""  # zone

    def move(self, event, a, b):
        """move on zone with x,y"""
        a, b = [sum(x) for x in zip((a, b), self.position[0])]
        if (a, b) not in self.univers.wall.position and a in range(self.univers.width) and b in range(self.univers.width):
            self.set_position = [a, b]
            self.univers.draw_entity(self)
            [self.objet_in_case(obj) for obj in self.univers.tab_objet]
            self.end_game()

    def objet_in_case(self, objet):
        """ test if character on objet , if true  =>> in the bag"""
        if self.position == objet.position:
            self.univers.zone_c.delete(objet.locate)
            self.bag[objet.name] = objet
            self.univers.tab_objet.remove(objet)
            threading.Thread(None, self.univers.counter_see,
                             None, (self.bag,)).start()

    def end_game(self):
        """ Desactivates commands and displays the result of the game if one is at the end"""
        if self.position == self.univers.guardian.position:
            if len(self.bag) == 3:
                self.univers.zone_c.delete(self.univers.guardian.locate)
                texte = "You win !!!!!!"
            else:
                self.univers.zone_c.delete(self.locate)
                texte = "You Lose !!!!!!!!!"
            self.txt = self.univers.zone_c.create_text(int(self.univers.width * self.univers.dimension_sprite / 2), int(
                self.univers.width * self.univers.dimension_sprite / 2), text=texte, font="Arial 16 italic bold", fill="white")
            self.univers.zone_c.update()
            time.sleep(2)
            self.univers.desactiv_command()

    @property
    def bag(self):
        """return the dict"""
        return self.dict_bag

    def add_bag(self, nom, pos):
        """ store objet"""
        self.dict_bag[nom] = pos
