#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading
from Gui import *

class StadeEauVive():

	MODE_INITIATION = 1
	MODE_ENTRAINEMENT = 2
	MODE_COMPETITION = 3

	NIVEAU_VANNES_MAX = 3.5
	NIVEAU_MIN_OMNIFLOT = 1.5
	NIVEAU_MIN_STOCKVIDE = 0

	mode = False
	gui = Gui()

	attenteActionGerant = False
	actionGerantEffectuee = False

	seanceOuverte = False
	mareeDescendante = True

	tempsEcoule = 0
	phase = 0

	volumeEauReserve = 0
	niveauReserve = 1. # en metres NGF
	niveauReserveMax = 1. # en metres NGF

	niveauVanneOmniflot = 1. # en metres NGF
	niveauVanneStockvide = 1. # en metres NGF

	niveauMerMin = 1. # en niveau hydrographique
	niveauMer = 1. # en niveau hydrographique
	niveauMerMax = 1. # en niveau hydrographique

	coefficientMaree = 0.

	vitesse = 60
	debit = 0

	def calculerNiveauMerMax(self):
		if self.coefficientMaree == 45:
			self.niveauMerMax = 7.
			self.niveauMer = 7.
			self.niveauMerMin = 3.
		elif self.coefficientMaree == 60:
			self.niveauMerMax = 8.
			self.niveauMer = 8.
			self.niveauMerMin = 2.
		else:
			self.niveauMerMax = 9.
			self.niveauMer = 9.
			self.niveauMerMin = 1.

	def calculerNiveauMer(self):
		c = ((self.niveauMerMax - self.niveauMerMin) / 360) * self.vitesse

		if self.mareeDescendante:
			self.niveauMer -= c
		else:
			self.niveauMer += c

		if self.phase == 0:
			self.mareeDescendante = True
			self.niveauMer = self.niveauMerMax
		if self.phase == 6:
			self.mareeDescendante = False
			self.niveauMer = self.niveauMerMin

	def calculerNiveauVannes(self):
		if self.phase >= 0 and self.phase < 3:
			self.seanceOuverte = False
			self.actionGerantEffectuee = False
			self.niveauVanneOmniflot = self.niveauReserveMax 
			self.niveauVanneStockvide = self.NIVEAU_VANNES_MAX

		if self.phase == 3:
			if self.mode == self.MODE_INITIATION:
				self.niveauVanneOmniflot = self.niveauReserveMax - 0.4
			elif self.mode == self.MODE_ENTRAINEMENT:
				self.niveauVanneOmniflot = self.niveauReserveMax - 0.6
			else:
				self.niveauVanneOmniflot = self.niveauReserveMax - 0.9

		if self.phase > 3 and self.phase < 9:
			self.seanceOuverte = True

			if self.mode == self.MODE_INITIATION:
				self.niveauVanneOmniflot -= 0.001575 * self.vitesse
			elif self.mode == self.MODE_ENTRAINEMENT:
				self.niveauVanneOmniflot -= 0.004 * self.vitesse
			else:
				self.niveauVanneOmniflot -= 0.008 * self.vitesse

			if self.niveauVanneOmniflot < 1.5:
				self.niveauVanneOmniflot = 1.5

		if self.phase == 9:
			self.seanceOuverte = False

			if not self.actionGerantEffectuee:
				self.attenteActionGerant = True

	def calculerDebit(self):
		if self.mode == self.MODE_INITIATION:
			self.debit = 4
		elif self.mode == self.MODE_ENTRAINEMENT:
			self.debit = 9
		else:
			self.debit = 14

	def calculerNiveauReserveMax(self):
		self.niveauReserveMax = self.niveauMerMax - 5

		if self.niveauReserveMax > 3.5:
			self.niveauReserveMax = 3.5

	def calculerNiveauReserve(self):
		if self.phase < 9:
			if self.mode == self.MODE_INITIATION:
				self.niveauReserve = self.niveauVanneOmniflot + 0.4

			elif self.mode == self.MODE_ENTRAINEMENT:
				self.niveauReserve = self.niveauVanneOmniflot + 0.6

			else:
				self.niveauReserve = self.niveauVanneOmniflot + 0.9

			if self.niveauReserve > self.niveauReserveMax:
				self.niveauReserve = self.niveauReserveMax

			if self.niveauVanneOmniflot == self.NIVEAU_MIN_OMNIFLOT:
				self.niveauReserve = self.niveauVanneOmniflot

		elif self.phase >= 10:
			if self.niveauMer - 5 > 1.5:
				self.niveauReserve = self.niveauMer - 5

			if self.niveauReserve > 3.5:
				self.niveauReserve = 3.5

	def calculerPhase(self):
		self.phase = round(self.tempsEcoule / 60) % 12

	def actionGerant(self):
		if not self.attenteActionGerant:
			return

		entree = raw_input("Veuillez appuyer sur la touche entrée pour continuer")
		self.attenteActionGerant = False
		self.actionGerantEffectuee = True
		self.niveauVanneOmniflot = self.NIVEAU_MIN_OMNIFLOT
		self.niveauVanneStockvide = self.NIVEAU_MIN_STOCKVIDE
		self.niveauReserve = 0

	def affichage(self):

		self.gui.afficherReserve(self.niveauReserve)
		
		print "====================================="

		if self.seanceOuverte:
			print "== SEANCE OUVERTE"
		else:
			print "== SEANCE FERMÉE"

		print "== PHASE: PM+%d" % self.phase
		print "débit: %d m3/s" % self.debit
		print "niveau mer: %f" % self.niveauMer
		print "niveau mer max: %f" % self.niveauMerMax
		print "niveau réserve: %f" % self.niveauReserve
		print "niveau réserve max: %f" % self.niveauReserveMax

		if self.niveauVanneOmniflot == self.NIVEAU_VANNES_MAX:
			print "vanne omniflot fermée !"
		elif self.niveauVanneOmniflot == self.NIVEAU_MIN_OMNIFLOT:
			print "vanne omniflot affalée !"
		else:
			print "niveau vanne omniflot: %f" % self.niveauVanneOmniflot

		if self.niveauVanneStockvide == self.NIVEAU_VANNES_MAX:
			print "vanne stockvide fermée !"
		elif self.niveauVanneStockvide == self.NIVEAU_MIN_STOCKVIDE:
			print "vanne stockvide affalée !"
		else:
			print "niveau vanne stockvide: %f" % self.niveauVanneStockvide

		print "coeff marée: %f" % self.coefficientMaree
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
			choix = raw_input("Mode de fonctionnement ?: ")
			
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
			choix = raw_input("Coefficient de maree ? (45, 60, 95): ")
		
		self.coefficientMaree = int(choix)

		vit = 0
		print "Veuillez choisir une vitesse de rafraichissement en minutes / 3 sec: "
		
		while vit == "" or int(vit) < 1 or int(vit) > 60:
			vit = raw_input("Vitesse ? (entre 1 et 60): ")

		self.vitesse = int(vit) 

		self.simulation()

	def simulation(self):
		print "Debut de la simulation."

		#entree = threading.Thread(target=self.lireEntree)
		#entree.daemon = True
		#entree.start()

		self.calculerNiveauMerMax()
		self.calculerNiveauReserveMax()
		self.calculerDebit()

		while 1:
			self.tempsEcoule += self.vitesse

			self.calculerPhase()
			self.calculerNiveauMer()
			self.calculerNiveauVannes()
			self.calculerNiveauReserve()

			self.affichage()

			self.actionGerant()

			time.sleep(3)

	def __init__(self):
		self.menu()
		

if __name__ == '__main__':
	StadeEauVive()
