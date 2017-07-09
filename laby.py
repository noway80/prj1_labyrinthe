#! /usr/bin/python
# -*- coding:Utf-8 -*-

from tkinter import *
import random


class Labyrinth_MG:

    def __init__(self, frame):
        """ init des variables"""
        self.dimension_sprite = 25
        self.width = 15
        self.picture_needle = PhotoImage(
            file='./images/aiguille.png')  # picture needle
        self.picture_syringe = PhotoImage(
            file='./images/seringue.png')  # picture syringe
        self.picture_ether = PhotoImage(
            file='./images/ether.png')  # picture wall
        self.picture_wall = PhotoImage(file='./images/mur.png')  # picture wall
        self.picture_mg = PhotoImage(
            file='./images/mg.png')  # picture mac giver
        self.picture_gd = PhotoImage(
            file='./images/gd.png')  # picture guardian
        self.frame = frame
        self.zone_c = Canvas(self.frame, width=self.width *
                             self.dimension_sprite, height=self.width * self.dimension_sprite)
        self.zone_c.bind("<space>", self.init_game)
        self.zone_c.bind("<Escape>", self.kill_game)
        self.im_fond = PhotoImage(file='./images/fond.png')
        self.zone_c.create_image(0, 0, anchor=NW, image=self.im_fond)
        self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2), int(
            self.width * self.dimension_sprite / 2), text='Press"SPACE" to Start !!!\r      "Echap" to quit', font="Arial 16 italic bold", fill="white")
        self.zone_c.pack()
        self.zone_c.focus_set()

        self.tab_position_objets = []  # position possible des objets
        self.tab_position_wall = []  # stock positions mur
        self.tab_position_character = []  # position des personnages
        self.tab_objets = []  # positions des objets

    def zone(self):
        """initialiser la zone"""
        file_in = "./zones/zone1.txt"  # carte avec les données
        y = 0
        with open(file_in, 'r') as f:
            for line in f:
                for x in range(self.width):
                    if line[x] == " ":  # wall position
                        self.draw_brick(x * self.dimension_sprite,
                                        y * self.dimension_sprite)
                        self.tab_position_wall.append(
                            (x, y))  # stock position wall
                    elif line[x] == "O":  # position possible object
                        self.tab_position_objets.append((x, y))
                    elif line[x] == "P":  # position possible mac giver guardian
                        self.tab_position_character.append([x, y])
                y += 1

    def init_game(self, event):
        """ init des objets et des personnages , mise en place des commandes"""
        print("ok")
        self.zone_c.unbind('<space>')
        self.zone_c.delete(self.txt)
        self.zone()

        self.tab_objets.append(self.tab_position_objets.pop(
            random.randint(0, len(self.tab_position_objets) - 1)))  # position aiguille
        self.tab_objets.append(self.tab_position_objets.pop(random.randint(
            0, len(self.tab_position_objets) - 1)))  # position tranquilisant
        self.tab_objets.append(self.tab_position_objets.pop(random.randint(
            0, len(self.tab_position_objets) - 1)))  # position tube plastique
        self.position_mac_giver = self.tab_position_character[0]
        self.position_guardian = self.tab_position_character[1]
        self.draw_mac_giver(self.position_mac_giver)
        self.draw_guardian(self.position_guardian)
        self.draw_objet(self.tab_objets)

        # creation des map des touches pour mouvements
        self.zone_c.bind("<Right>", lambda e, a=1, b=0: self.move(e, a, b))
        self.zone_c.bind("<Left>", lambda e, a=-1, b=0: self.move(e, a, b))
        self.zone_c.bind("<Up>", lambda e, a=0, b=-1: self.move(e, a, b))
        self.zone_c.bind("<Down>", lambda e, a=0, b=1: self.move(e, a, b))

    def draw_brick(self, x, y):
        """ dessiner une brique du labyrinthe"""                                                #
        self.zone_c.create_image(x, y, anchor=NW, image=self.picture_wall)

    def draw_mac_giver(self, t):
        """ dessiner Mac Gyver"""
        self.mac_giver = self.zone_c.create_image(
            t[0] * self.dimension_sprite, t[1] * self.dimension_sprite, anchor=NW, image=self.picture_mg)

    def draw_objet(self, t_obj):
        """dessinez les objets et creation ref des objets"""
        self.dict_ref_objet = {}
        self.dict_ref_objet[(t_obj[0][0], t_obj[0][1])] = self.zone_c.create_image(t_obj[0][0] * self.dimension_sprite, t_obj[0][1]  # dict ref objey
                                                                                   * self.dimension_sprite, anchor=NW, image=self.picture_needle)
        self.dict_ref_objet[(t_obj[1][0], t_obj[1][1])] = self.zone_c.create_image(t_obj[1][0] * self.dimension_sprite, t_obj[1][1]
                                                                                   * self.dimension_sprite, anchor=NW, image=self.picture_syringe)
        self.dict_ref_objet[(t_obj[2][0], t_obj[2][1])] = self.zone_c.create_image(t_obj[2][0] * self.dimension_sprite, t_obj[2][1]
                                                                                   * self.dimension_sprite, anchor=NW, image=self.picture_ether)

    def draw_guardian(self, t):
        """ dessinez le gardien"""
        self.guardian = self.zone_c.create_image(t[0] * self.dimension_sprite, t[1]
                                                 * self.dimension_sprite, anchor=NW, image=self.picture_gd)

    def move(self, event, a, b):
        """deplacement de mac giver"""
        a += self.position_mac_giver[0]
        b += self.position_mac_giver[1]
        if (a, b) not in self.tab_position_wall and a in range(self.width) and b in range(self.width):  # test si mur ou hors jeu
            self.zone_c.delete(self.mac_giver)  # delete mac giver
            self.position_mac_giver[0] = a
            self.position_mac_giver[1] = b           
            self.draw_mac_giver(self.position_mac_giver) # create mac giver new position
            if tuple(self.position_mac_giver) in self.tab_objets:  # test si objet dans position de mac giver
                a = self.tab_objets.pop(self.tab_objets.index(
                    tuple(self.position_mac_giver)))  # reste objet a recuperer
                self.zone_c.delete(self.dict_ref_objet[a])  # desruction objet
            if self.position_mac_giver == self.position_guardian:
            	self.zone_c.unbind('<Up>')
            	self.zone_c.unbind('<Down>')
            	self.zone_c.unbind('<Left>')
            	self.zone_c.unbind('<Right>')            	
            	if len(self.tab_objets) ==0:
            		self.zone_c.delete(self.guardian)            		           		            	
            		texte= "You win !!!!!!"
            	else:
            		self.zone_c.delete(self.mac_giver)             	
            		texte="You Lose !!!!!!!!!"
            	self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2), int(
            self.width * self.dimension_sprite / 2), text=texte, font="Arial 16 italic bold", fill="white")
            	


    def kill_game(self, event):
        """ closed game"""
        self.frame.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title('Labyrinthe 0.2')
    widget = Labyrinth_MG(root)
    root.mainloop()
