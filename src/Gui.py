#!/usr/bin/python
# -*- coding: utf-8 -*-

import string

class Gui():

    draw = ""
    phase = 0

    def __init__(self):
        print "init"

    def afficherReserve(self, niveauReserve, niveauVanneOmniflot, phase):
        self.phase = phase
        self.draw = '''                         reserve
        |                                         
        |                                         
        |                                         
        |                                         
        |                                         
        |                                         
        |                                         
        |                                         
        |                                         
        |_________________________________________


        '''

        tab = string.split(self.draw, '\n')

        niveauMax = 35

        niveau = int(round( (niveauMax - (niveauReserve * 10)) / 2))

        if niveau <= 0:
            niveau = 1

        if niveau >= 9:
            niveau = 9

        if niveauReserve > 0:
            tab[niveau] = "        |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        self.draw = string.join(tab, '\n')

        self.afficherVanneOmniflot(niveau, niveauVanneOmniflot)

    def afficherVanneOmniflot(self, niveauReserve, niveauVanneOmniflot):

        vanne = '''
|
|
|
|
|
|
|
|
|
|
|
|
        '''

        if self.phase > 9 and self.phase < 12:
            niveauVanne = 9
        elif self.phase >= 1 and self.phase <= 3:
            niveauVanne = 1
        else:
            niveauVanne = niveauReserve

        niveauVanneMax = 9
        
        tabReserve = string.split(self.draw, '\n')
        tabVanne = string.split(vanne, '\n')

        for s in range(0, len(tabReserve)):
            if s >= niveauVanne:
                tabReserve[s] += tabVanne[s]

        self.draw = string.join(tabReserve, '\n')

        self.afficherStade()

    def afficherStade(self):
        stade = '''                    stade 








___ 
   \\
    \\___
    
        '''

        tab = string.split(self.draw, '\n')
        tabStade = string.split(stade, '\n')

        for s in range(0, len(tab)):
            tab[s] += tabStade[s]

        self.draw = string.join(tab, '\n')
        print self.draw

