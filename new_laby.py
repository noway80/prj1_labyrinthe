#!/usr/bin/python3
# -*- coding: Utf-8 -*


from tkinter import *
import random
import time
from labyrinthe.entity import Objet
from labyrinthe.character import Character
from labyrinthe.zone import Zone
from labyrinthe.decor import Decor

if __name__ == '__main__':
    wall = Decor('./images/mur.png', "Wall")
    plastic_tube = Objet('./images/plastic_tube.png', "Plastic Tube")
    needle = Objet('./images/aiguille.png', "Needle")
    ether = Objet('./images/ether.png', "Ether")
    mac_giver = Character('./images/mg.png', "Mac Gyver")
    guardian = Character('./images/gd.png', "Mac Gyver")
    cartes = ["./zones/zone1.txt", "./zones/zone2.txt",
              "./zones/zone3.txt"]  # Map with data
    #cartes=[]
    objet = [plastic_tube, needle, ether]
    character = [mac_giver, guardian]
    root = Tk()
    root.title('New Labyrinthe 0.3')
    widget = Zone(root, objet, character, wall, cartes)
    root.mainloop()
