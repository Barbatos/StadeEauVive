#!/usr/bin/python

import string

class Gui():

    def __init__(self):
        print "init"

    def afficherReserve(self, niveauReserve):
        reserve = '''
        |                                         |
        |                                         |
        |                                         |
        |                                         |
        |                                         |
        |                                         |
        |                                         |
        |_________________________________________|
        '''

        tab = string.split(reserve, '\n')

        if niveauReserve > 0:
            tab[-(niveauReserve+2)] = "        |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|"

        reserve = string.join(tab, '\n')
        print reserve

    def afficherEauReserve(self):
        print "a"
        #print '''
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #'''