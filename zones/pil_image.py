#-------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      serge
#
# Created:     30/11/2016
# Copyright:   (c) serge 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------
#! /usr/bin/python
# -*- coding:Utf-8 -*-

import PIL.Image
import os
import numpy
import pygame


def create_tableau_labyrinthe_bit(infile):
    """ creation coordonnées du labyrinthe dans un tableau de bit (16,255,85....)"""
    i = PIL.Image.open(infile)
    hauteur = i.size[1]
    largeur = i.size[0]
    tab_image = []
    for a in range(hauteur):
        bit = 0
        for b in range(largeur):
            # Returns the color level (coded in 16 levels therefore 0 to 15) /
            c = PIL.Image.Image.getpixel(i, (b, a))
            # renvoi le niveau de couleur (codé en 16 niveaux donc 0 a 15 )
            if c < 10:  # road / chemin
                valeur_pixel = 1
            else:  # Wall / mur
                valeur_pixel = 0
            bit <<= 1
            bit += valeur_pixel
        if largeur % 8 != 0:
            bit <<= 1
        tab_image.append(bit >> 8)
        tab_image.append(bit & 255)
    return tuple(tab_image)


def create_file_labyrinthe_txt(infile):
    """ creation coordonnées du labyrinthe dans un fichier txt "O" pour objet,
     "i" pour chemin et "P" pour départ ou arrivée"""
    i = PIL.Image.open(infile)
    hauteur = i.size[1]
    largeur = i.size[0]
    fileout_txt = '%s.txt' % os.path.splitext(infile)[0]
    # file(fileout_txt, 'w').write
    with open(fileout_txt, 'w') as f:
        for a in range(hauteur):  # hauteur
            for b in range(largeur):  # largeur
                # Returns the color level (coded in 16 levels therefore 0 to
                # 15) /# renvoi le niveau de couleur (codé en 16 niveaux donc 0
                # a 15 )
                c = PIL.Image.Image.getpixel(i, (b, a))
                if c in [8, 9, 10]:  # position possible objet
                    bit = 'O'
                elif c <= 4:  # road / chemin
                    bit = 'l'
                # Possible position departure - arrived/ position possible départ
                # et arrivée
                elif c in [5, 6, 7]:
                    bit = 'P'
                else:  # Wall / mur
                    bit = ' '
                f.write(bit)
            f.write('\n')
    f.closed


def create_tableau_labyrinthe(infile):
    """ creation coordonnées du labyrinthe dans un tableau """
    i = PIL.Image.open(infile)
    hauteur = i.size[1]
    largeur = i.size[0]
    tab_image = []
    for a in range(hauteur):
        for b in range(largeur):
            c = PIL.Image.Image.getpixel(i, (b, a))# Returns the color level /
            #(coded in 16 levels therefore 0 to 15) /
            # renvoi le niveau de couleur (codé en 16 niveaux donc 0 a 15 )
            if c in [8, 9, 10]:  # position possible objet
                valeur_pixel = 3
            elif c <= 4:  # road / chemin
                valeur_pixel = 1
            # Possible position departure - arrived/ position possible départ
            # et arrivée
            elif c in [5, 6, 7]:
                valeur_pixel = 2
            else:  # Wall / mur
                valeur_pixel = 0
            tab_image.append(valeur_pixel)
    tab_image_numpy = numpy.array(tab_image)
    tab_image_numpy.shape = (hauteur, largeur)
    return tab_image_numpy


def main():
    print(create_tableau_labyrinthe_bit("zone1.bmp"))
    create_file_labyrinthe_txt("zone1.bmp")
    print(create_tableau_labyrinthe("zone1.bmp"))

if __name__ == '__main__':
    main()
