#!/usr/bin/python3
# -*- coding: Utf-8 -*

from tkinter import *
import random
import time
import threading
from tkinter import messagebox



class Zone:

    def __init__(self, frame,objet,character,wall):
        """ init variables"""
        self.frame = frame
        self.dimension_sprite = 25
        self.width = 15  # number of cases
        frame.resizable(False, False)
        self.zone_c = Canvas(self.frame, width=self.width *
                             self.dimension_sprite, height=self.width * self.dimension_sprite)
        self.zone_c.bind("<space>", self.init_game)
        self.zone_c.bind("<Escape>", self.kill_game)
        self.im_fond = PhotoImage(file='./images/fond.png')
        self.map_game = ["./zones/zone1.txt", "./zones/zone2.txt",
                             "./zones/zone3.txt"]
        self.zone_c.create_image(0, 0, anchor=NW, image=self.im_fond)
        self.txt = self.zone_c.create_text(int(self.width * self.dimension_sprite / 2), int(
            self.width * self.dimension_sprite / 2), text='Press"SPACE" to Start !!!\r      "Echap" to quit', font="Arial 16 italic bold", fill="white")
        self.zone_c.pack()
        self.zone_c.focus_set()
        self.tab_objet=objet
        self.mac_giver=character[0]
        self.guardian=character[1]
        self.wall=wall
        # Map with data
        self.aff = False  # Flag to avoid double display of counter

    def crea_zone(self, file_in):
        """Initialize the zone and create lists of data of the locations of the characters, objects and wall"""
        y = 0
        tab_position_objets=[]
        tab_position_character=[]
        with open(file_in[random.randint(0, len(file_in) - 1)], 'r') as f:
            for line in f:
                for x in range(self.width):
                    if line[x] == " ":  # wall position x,y
                        self.wall.add_position((x, y))  # stock position wall
                    elif line[x] == "O":  # position possible object
                        tab_position_objets.append([x, y])
                    elif line[x] == "P":  # position possible mac giver guardian
                        tab_position_character.append([x, y])
                y += 1
        self.draw_entity(self.wall)
        for obj in self.tab_objet:
            obj.set_position= tab_position_objets.pop(random.randint(0, len(tab_position_objets) - 1))
            self.draw_entity(obj)
        self.mac_giver.set_position=tab_position_character[0]
        self.draw_entity(self.mac_giver)
        self.guardian.set_position=tab_position_character[1]
        self.draw_entity(self.guardian)


    def init_game(self, event):
        """ Init objects and characters, set up commands"""
        self.zone_c.unbind('<space>')
        self.zone_c.delete(self.txt)
        self.crea_zone(self.map_game)        
        # Creation of map of the keys for movements
        self.zone_c.bind("<Right>", lambda e, a=1, b=0: self.mac_giver.move(e, a, b))
        self.zone_c.bind("<Left>", lambda e, a=-1, b=0: self.mac_giver.move(e, a, b))
        self.zone_c.bind("<Up>", lambda e, a=0, b=-1: self.mac_giver.move(e, a, b))
        self.zone_c.bind("<Down>", lambda e, a=0, b=1: self.mac_giver.move(e, a, b))
        self.mac_giver.univers=self
    
   
    def draw_entity(self,entity):
        """ draw the wall labyrinthe with list position x,y and picture"""
        entity.photoimage=PhotoImage(file=entity.photo)
        #print(entity.position)
        for ent in entity.position:      
            entity.locate=self.zone_c.create_image(ent[0]* self.dimension_sprite, ent[1]* self.dimension_sprite, anchor=NW, image=entity.photoimage)

    def affiche_compteur(self,obj):
        """ display count objets"""
        bag=obj.bag
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
        self.zone_c.unbind('<Up>')
        self.zone_c.unbind('<Down>')
        self.zone_c.unbind('<Left>')
        self.zone_c.unbind('<Right>')

    def kill_game(self, event):
        """ closed game"""
        self.frame.destroy()



class Objet:

    def __init__(self,nom_image,nom):
        self.set_position=[0,0]
        self.photo=nom_image
        self.photoimage=""
        self.name=nom
        self.locate=""

    @property
    def position(self):
    	return [self.set_position]
	    
    
class Decor:

    def __init__(self,nom_image,nom):
        self.tab_position=[]
        self.photo=nom_image
        self.photoimage=""
        self.name=nom
        self.locate=""
	    
    def add_position(self,pos):
	    self.tab_position.append(pos)
    
    @property
    def position(self):
    	return self.tab_position



class Character:
	
    def __init__(self,nom_image,nom):
        self.set_position=[0,0]
        self.photo=nom_image
        self.name=nom
        self.dict_bag={}
        self.univers=""
        self.locate=""

    def move(self,event,a,b):
        a, b = [sum(x) for x in zip((a, b), self.position[0])]
        if (a, b) not in self.univers.wall.position and a in range(self.univers.width) and b in range(self.univers.width):
            
            self.set_position=[a,b]
            self.univers.draw_entity(self)
            for obj in self.univers.tab_objet:
            	self.objet_in_case(obj) 
            self.end_game()
    
    def objet_in_case(self,objet):
       if self.position== objet.position:
       		self.univers.zone_c.delete(objet.locate)
       		self.bag[objet.name]=objet.position
       		self.univers.tab_objet.remove(objet)
       		threading.Thread(None, self.univers.affiche_compteur,None,(self,)).start()

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
        return self.dict_bag
    
    def add_bag(self,nom,pos):
    	self.dict_bag[nom]=pos

    @property
    def position(self):
    	return [self.set_position]
	
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