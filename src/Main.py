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


	niveauReserve = 1 # en metres NGF
	niveauReserveMax = 1 # en metres NGF

	niveauVanneOmniflot = 1 # en metres NGF
	niveauVanneStockvide = 1 # en metres NGF

	niveauMerMin = 1 # en niveau hydrographique
	niveauMer = 1 # en niveau hydrographique
	niveauMerMax = 1 # en niveau hydrographique

	coefficientMaree = 0

	vitesse = 15

	def calculerNiveauMerMax(self):
		if self.coefficientMaree == 45:
			self.niveauMerMax = 7
			self.niveauMerMin = 3
		elif self.coefficientMaree == 60:
			self.niveauMerMax = 8
			self.niveauMerMin = 2
		else:
			self.niveauMerMax = 9
			self.niveauMerMin = 1

	#def calculerNiveauMer(self):


	def calculerNiveauReserveMax(self):
		self.niveauReserveMax = self.niveauMerMax - 5

		if self.niveauReserveMax > 3.5:
			self.niveauReserveMax = 3.5


	def affichage(self):
		#self.gui.afficherReserve(self.niveauReserve)
		print "====================================="
		print "== SEANCE: "
		print "niveau mer: %d" % self.niveauMer
		print "niveau mer max: %d" % self.niveauMerMax
		print "niveau réserve: %d" % self.niveauReserve
		print "niveau réserve max: %d" % self.niveauReserveMax
		print "niveau vanne omniflot: %d" % self.niveauVanneOmniflot
		print "niveau vanne stockvide: %d" % self.niveauVanneStockvide
		print "coeff maree: %d" % self.coefficientMaree
		print "====================================="

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

		time.sleep(0.1)


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

		print "Veuillez choisir un coefficient de maree: "
		
		while choix != "45" and choix != "60" and choix != "95":
			choix = raw_input("Coefficient de maree ? (45, 60, 95)")
		
		self.coefficientMaree = int(choix)

		self.simulation()

	def simulation(self):
		print "Debut de la simulation."

		entree = threading.Thread(target=self.lireEntree)
		entree.daemon = True
		entree.start()

		self.calculerNiveauMerMax()
		self.calculerNiveauReserveMax()

		while 1:
			self.affichage()
			time.sleep(2)

	def __init__(self):
		self.menu()
		

if __name__ == '__main__':
	StadeEauVive()
