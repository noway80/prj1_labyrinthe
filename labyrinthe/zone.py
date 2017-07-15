#!/usr/bin/python3
# -*- coding: Utf-8 -*

import random
import time
from tkinter import messagebox
from tkinter import *


class Zone:

    def __init__(self, frame, objet, character, wall, map_game):
        """ init variables"""
        self.frame = frame
        frame.resizable(False, False)
        try:
            self.dimension_sprite = 25
            if len(map_game) == 0:
                self.width = 17
            else:
                self.width = 15  # number of case
            self.im_fond = PhotoImage(file='./images/fond.png')
            self.map_game=map_game  #map labyrinth
        except Exception as e:
            messagebox.showinfo("Error Config", "Erreur : {}".format(e))
            self.frame.destroy()
        self.zone_c = Canvas(self.frame, width=self.width *
                             self.dimension_sprite, height=self.width * self.dimension_sprite)
        self.zone_c.create_image(0, 0, anchor=NW, image=self.im_fond)
        self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2),
                             int(self.width * self.dimension_sprite / 2), 
                                    text='Press"SPACE" to Start !!! \r      "Echap" to quit', 
                                                     font="Arial 16 italic bold", fill="white")
        self.zone_c.bind("<space>", self.init_game)
        self.zone_c.bind("<Escape>", self.kill_game)
        self.zone_c.pack()
        self.zone_c.focus_set()
        self.tab_objet = objet
        self.tab_character = character
        self.mac_giver = self.tab_character[0]
        self.guardian = self.tab_character[1]
        self.wall = wall
        self.aff = False  # Flag to avoid double display of counter

    def crea_zone(self, file_in):
        """Initialize the zone and create lists of data of /
        the locations of the characters, objects and wall with file"""
        y = 0
        tab_position_objets = []
        tab_position_character = []
        if len(file_in) > 0:
            with open(file_in[random.randint(0, len(file_in) - 1)], 'r') as f:
                for line in f:
                    for x in range(self.width):
                        if line[x] == " ":  # wall position x,y
                            self.wall.add_position((x, y))  # stock position wall
                        elif line[x] == "O":  # position possible object
                            tab_position_objets.append([x, y])
                        elif line[x] == "P":  # position possible macgiver guardian
                            tab_position_character.append([x, y])
                    y += 1
        else:
            f = self.make_labyrinth(self.width)
            for line in f:
                for x in range(len(line)):
                    if line[x] == "t":  # wall position x,y
                        self.wall.add_position((x, y))  # stock position wall
                    elif line[x] == "P":  # position possible mac giver guardian
                        tab_position_character.append([x, y])
                    else:  # position possible object
                        tab_position_objets.append([x, y])
                y += 1

        self.draw_entity(self.wall)
        for obj in self.tab_objet:
            obj.set_position = tab_position_objets.pop(
                random.randint(0, len(tab_position_objets) - 1))
            self.draw_entity(obj)
        self.mac_giver.set_position = tab_position_character[0]
        self.draw_entity(self.mac_giver)
        self.guardian.set_position = tab_position_character[1]
        self.draw_entity(self.guardian)

    def make_labyrinth(self, v):
        """To make a labyrinth with algorithm random fusion """
        nb = 0
        tab_mur = []
        tab_chemin_init = []
        tt = [["t" for a in range(v)]
              for x in range(v)]  # new labyrinth
        for x, t1 in enumerate(tt):  # path init
            for y, t2 in enumerate(t1):
                if x % 2 != 0:
                    if y % 2 != 0:
                        tt[x][y] = '{}'.format(nb)
                        nb += 1
                        tab_chemin_init.append((x, y))
                    else:
                        if y != 0 and y != (len(tt) - 1):
                            tab_mur.append((x, y))
                else:
                    if x != 0 and x != (len(tt) - 1):
                        tab_mur.append((x, y))
        tab_mur.remove((v - 3, v - 2)) #Security construction object
        tab_mur.remove((2, 1))  # security init "start"
        while len(tab_mur) > 0:  # make labyrinth with algo
            a, b = tab_mur.pop(random.randint(0, len(tab_mur) - 1))
            if tt[a][b] == 't':
                if a % 2 == 0:
                    v1 = tt[a - 1][b]
                    v2 = tt[a + 1][b]
                else:
                    v1 = tt[a][b - 1]
                    v2 = tt[a][b + 1]
                if v1 != 't' and v2 != 't' and v1 != v2:
                    for i, t1 in enumerate(tt):
                        for j, t in enumerate(t1):
                            if t == v2:
                                tt[i][j] = v1
                                tt[a][b] = v1
        for pos in range(0, -2, -1):  # make "start" and "end"
            t = tab_chemin_init.pop(pos)
            tt[t[0]][t[1]] = "P"
        return tt

    def init_game(self, event):
        """ Init objects and characters, set up commands"""
        self.zone_c.unbind('<space>')
        self.zone_c.delete(self.txt)
        self.crea_zone(self.map_game)
        # Creation of map of the keys for movements
        self.zone_c.bind("<Right>", lambda e, a=1,
                         b=0: self.mac_giver.move(e, a, b))
        self.zone_c.bind("<Left>", lambda e, a=-1,
                         b=0: self.mac_giver.move(e, a, b))
        self.zone_c.bind("<Up>", lambda e, a=0, b=-
                         1: self.mac_giver.move(e, a, b))
        self.zone_c.bind("<Down>", lambda e, a=0,
                         b=1: self.mac_giver.move(e, a, b))
        self.mac_giver.univers = self

    def draw_entity(self, entity):
        """ draw entity labyrinthe with list position x,y and picture"""
        entity.photoimage = PhotoImage(file=entity.photo)
        for ent in entity.position:
            entity.locate = self.zone_c.create_image(
                ent[0] * self.dimension_sprite, ent[1] * self.dimension_sprite, anchor=NW, image=entity.photoimage)
            # print(entity.locate)

    def counter_see(self, bag):
        """ display count objets and name"""
        while self.aff == True:
            time.sleep(0.1)
        self.aff = True
        texte = "{}  find \n".format(", ".join([x for x in bag.keys()]))
        if len(bag) == 3:
            texte += "       You can escape ...."
        for coul in ["white", "red", "white"]:
            self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2), int(
                self.width * self.dimension_sprite / 2), text=texte, font="Arial 16 italic bold", fill=coul)
            time.sleep(0.7)
            self.zone_c.delete(self.txt)
        self.aff = False

    def desactiv_command(self):
        """ desactiv command for move"""
        self.zone_c.unbind('<Up>')
        self.zone_c.unbind('<Down>')
        self.zone_c.unbind('<Left>')
        self.zone_c.unbind('<Right>')
        # re-init
        self.wall.tab_position = []
        for obj in self.mac_giver.bag.values():
            self.tab_objet.append(obj)
        self.mac_giver.dict_bag = {}
        self.zone_c.delete(ALL)
        self.zone_c.create_image(0, 0, anchor=NW, image=self.im_fond)
        self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2), int(
            self.width * self.dimension_sprite / 2), text='Press"SPACE" to Start !!!\r      "Echap" to quit', font="Arial 16 italic bold", fill="white")
        self.zone_c.bind("<space>", self.init_game)

    def kill_game(self, event):
        """ closed game"""
        self.frame.destroy()
