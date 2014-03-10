#!/usr/bin/python

class StadeEauVive():

	MODE_INITIATION = 1
	MODE_ENTRAINEMENT = 2
	MODE_COMPETITION = 3
	mode = False

	def menu(self):
		print '''
	Bienvenue sur le simulateur du Stade d'Eau Vive.
	Veuillez choisir le mode de fonctionnement :
		1 - Initiation
		2 - Entrainement
		3 - Competition
		'''

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

		self.demarrerSimulation()

	def demarrerSimulation(self):
		print "Debut de la simulation."

	def __init__(self):
		self.menu()
		

if __name__ == '__main__':
	StadeEauVive()
