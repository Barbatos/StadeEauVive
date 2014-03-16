#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading
from Gui import *

class StadeEauVive():

	MODE_INITIATION = 1
	MODE_ENTRAINEMENT = 2
	MODE_COMPETITION = 3
	mode = False
	gui = Gui()
	niveauReserve = 1
	vitesse = 15
	coefficientMaree = 60

	def affichage(self):
		self.gui.afficherReserve(self.niveauReserve)

	def lireEntree(self):
		while 1:
			entree = raw_input("")
			if entree:
				if entree == "-":
					self.vitesse /= 2

					if self.vitesse < 1:
						self.vitesse = 1

					print "Vitesse: %s minute(s) par seconde" % self.vitesse

				if entree == "+":
					self.vitesse *= 2

					if self.vitesse > 60:
						self.vitesse = 60

					print "Vitesse: %s minute(s) par seconde" % self.vitesse


	def menu(self):
		print '''
	Bienvenue sur le simulateur du Stade d'Eau Vive.

	Vitesse actuelle: %s mins par seconde.
	Pour changer la vitesse, utilisez + et -

	Veuillez choisir le mode de fonctionnement :
		1 - Initiation
		2 - Entrainement
		3 - Competition
		''' % self.vitesse

		while self.mode == False:
			choix = raw_input("Mode de fonctionnement ? ")
			
			if choix == "1":
				self.mode = self.MODE_INITIATION
			elif choix == "2":
				self.mode = self.MODE_ENTRAINEMENT
			elif choix == "3":
				self.mode = self.MODE_COMPETITION
			else:
				print "Ce mode est invalide."

		self.simulation()

	def simulation(self):
		print "Debut de la simulation."

		entree = threading.Thread(target=self.lireEntree)
		entree.daemon = True
		entree.start()

		while 1:
			self.affichage()
			time.sleep(2)

	def __init__(self):
		self.menu()
		

if __name__ == '__main__':
	StadeEauVive()
