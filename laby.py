#!/usr/bin/python3
# -*- coding: Utf-8 -*

from tkinter import *
import random
import time
import threading


class Labyrinth_MG:

    def __init__(self, frame):
        """ init variables"""
        self.dimension_sprite = 25
        self.width = 15  # number of cases
        self.picture_needle = PhotoImage(
            file='./images/aiguille.png')  # picture needle
        self.picture_syringe = PhotoImage(
            file='./images/seringue.png')  # picture syringe
        self.picture_ether = PhotoImage(
            file='./images/ether.png')  # picture ether
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
        self.dict_ref_objet = {} #dictionnary of objets with ref and position
        self.tab_position_objets = []  # position possible objet
        self.tab_position_wall = []  # stock positions wall
        self.tab_position_character = []  # position character

        self.aff = False  # Flag to avoid double display of counter

    def zone(self):
        """Initialize the zone and create lists of data of the locations of the characters, objects and wall"""
        file_in = ["./zones/zone1.txt", "./zones/zone2.txt",
                   "./zones/zone3.txt"]  # carte avec les données
        y = 0
        with open(file_in[random.randint(0, len(file_in) - 1)], 'r') as f:
            for line in f:
                for x in range(self.width):
                    if line[x] == " ":  # wall position x,y
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
        """ Init objects and characters, set up commands"""
        self.zone_c.unbind('<space>')
        self.zone_c.delete(self.txt)
        self.zone()
        self.position_mac_giver = self.tab_position_character[0]
        self.position_guardian = self.tab_position_character[1]
        self.draw_mac_giver(self.position_mac_giver, self.picture_mg)
        self.draw_guardian(self.position_guardian)
        self.draw_objet(self.tab_position_objets)
        # Creation of map of the keys for movements
        self.zone_c.bind("<Right>", lambda e, a=1, b=0: self.move(e, a, b))
        self.zone_c.bind("<Left>", lambda e, a=-1, b=0: self.move(e, a, b))
        self.zone_c.bind("<Up>", lambda e, a=0, b=-1: self.move(e, a, b))
        self.zone_c.bind("<Down>", lambda e, a=0, b=1: self.move(e, a, b))

    def draw_brick(self, x, y):
        """ draw the wall labyrinthe with position x,y"""                                                #
        self.zone_c.create_image(x, y, anchor=NW, image=self.picture_wall)

    def draw_mac_giver(self, t, img):
        """ draw mac giver with position x and y and picture"""
        self.mac_giver = self.zone_c.create_image(
            t[0] * self.dimension_sprite, t[1] * self.dimension_sprite, anchor=NW, image=img)

    def draw_objet(self, t_obj):
        """Draw objects and create ref objects in a dictionary to erase later"""
        tab_pictures = [self.picture_needle,
                        self.picture_syringe, self.picture_ether]
        for i in range(len(tab_pictures)):
            pos = t_obj.pop(random.randint(0, len(t_obj) - 1))
            self.dict_ref_objet[pos] = self.zone_c.create_image(
                pos[0] * self.dimension_sprite, pos[1] * self.dimension_sprite, anchor=NW, image=tab_pictures[i])

    def draw_guardian(self, t):
        """ draw the guardian with position"""
        self.guardian = self.zone_c.create_image(t[0] * self.dimension_sprite, t[1]
                                                 * self.dimension_sprite, anchor=NW, image=self.picture_gd)

    def move(self, event, a, b):
        """Move mac giver , recept x et y = 0,1 ou -1 and recalculates position"""
        # print(self.zone_c.coords(self.mac_giver))
        a += self.position_mac_giver[0]
        b += self.position_mac_giver[1]
        if (a, b) not in self.tab_position_wall and a in range(self.width) and b in range(self.width):  # Test if wall or offside
            # Choice delete / create mac giver instead of "coords"
            # to change picture
            self.zone_c.delete(self.mac_giver)
            self.position_mac_giver = [a, b]
            # create mac giver new position
            self.draw_mac_giver(self.position_mac_giver, self.picture_mg)
            # test if object in position of mac giver
            self.objet_in_case(self.position_mac_giver)
            self.end_game(self.position_mac_giver)  # test end game

    def end_game(self, pos):
        """ Desactivates commands and displays the result of the game if one is at the end"""
        if pos == self.position_guardian:
            self.zone_c.unbind('<Up>')
            self.zone_c.unbind('<Down>')
            self.zone_c.unbind('<Left>')
            self.zone_c.unbind('<Right>')
            if len(self.dict_ref_objet) == 0:
                self.zone_c.delete(self.guardian)
                texte = "You win !!!!!!"
            else:
                self.zone_c.delete(self.mac_giver)
                texte = "You Lose !!!!!!!!!"
            self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2), int(
                self.width * self.dimension_sprite / 2), text=texte, font="Arial 16 italic bold", fill="white")

    def objet_in_case(self, pos):
        """ Test if object on the case and retrieve it"""
        pos = tuple(pos)
        if pos in self.dict_ref_objet.keys():
            self.zone_c.delete(self.dict_ref_objet[pos])
            self.dict_ref_objet.pop(pos)  # destroy objet
            threading.Thread(None, self.affiche_compteur).start()

    def affiche_compteur(self):
        """ dispaly count objets"""
        while self.aff == True:
            time.sleep(0.1)
        self.aff = True
        if len(self.dict_ref_objet) == 0:
            texte = "You can escape ...."
        else:
            texte = "{} more objects to find".format(len(self.dict_ref_objet))
        for coul in ["white", "red", "white"]:
            self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2), int(
                self.width * self.dimension_sprite / 2), text=texte, font="Arial 16 italic bold", fill=coul)
            time.sleep(0.7)
            self.zone_c.delete(self.txt)
        self.aff = False

    def kill_game(self, event):
        """ closed game"""
        self.frame.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title('Labyrinthe 0.3.3')
    widget = Labyrinth_MG(root)
    root.mainloop()
