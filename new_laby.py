#!/usr/bin/python3
# -*- coding: Utf-8 -*


from tkinter import *
import random
import time
from labyrinthe.entity import *
from labyrinthe.character import Character
from labyrinthe.zone import Zone
	
if __name__ == '__main__':
    wall=Decor('./images/mur.png',"Wall")
    seringe=Objet('./images/seringue.png',"Seringe")
    needle=Objet('./images/aiguille.png',"Needle")
    ether=Objet('./images/ether.png',"Ether")
    mac_giver=Character('./images/mg.png',"Mac Gyver")
    guardian=Character('./images/gd.png',"Mac Gyver")
    objet=[seringe,needle,ether]
    character=[mac_giver,guardian]
    root = Tk()
    root.title('New Labyrinthe 0.1')
    widget = Zone(root,objet,character,wall)
    root.mainloop()
    