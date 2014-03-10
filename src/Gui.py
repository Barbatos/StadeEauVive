#!/usr/bin/python
# -*- coding: utf-8 -*-

import string

class Gui():

    draw = ""

    def __init__(self):
        print "init"

    def afficherReserve(self, niveauReserve):
        self.draw = '''
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

        if niveauReserve > 0:
            tab[-(niveauReserve + 2)] = "        |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        self.draw = string.join(tab, '\n')

        self.afficherVanneOmniflot()

    def afficherVanneOmniflot(self):
        vanne = '''
       °
      / \\
     /   \\
    /     \\
   /       \\
  /         \\
 /           \\
/             °
        '''

        tabReserve = string.split(self.draw, '\n')
        tabVanne = string.split(vanne, '\n')

        for s in range(0, len(tabReserve)):
            tabReserve[s] += tabVanne[s]

        self.draw = string.join(tabReserve, '\n')

        print self.draw

