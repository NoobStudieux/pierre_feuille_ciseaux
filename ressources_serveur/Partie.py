#-*- coding=utf8 -*-

class Partie:
    def __init__(self, j1, j2):
        self.j1 = j1
        self.j2 = j2
        self.choixJ1 = None
        self.choixJ2 = None
        self.gagnant = None
        self.enCours = True
    def concourir(self2):
        if self.choixJ2 == self.choixJ2:
            print("egalite")
        elif self.choixJ1 == "pierre" and self.choixJ2 == "feuille":
	        self.setGagnant(j1.pseudo)
        elif self.choixJ1 == "feuille" and self.choixJ2 == "pierre":
	        self.setGagnant(j1.pseudo)
        elif self.choixJ1 == "ciseaux" and self.choixJ2 == "feuille":
	        self.setGagnant(j1.pseudo)
        else:
	        self.setGagnant(j2.pseudo)
    def setEgalite(self):
	    self.gagnant = "egalite"
    def setGagnant(self, pseudo_gagnant):
	    self.gagnant = pseudo_gagnant
    def setChoix(self, pseudo, choix):
        if pseudo == self.j1.pseudo:
            self.choixJ1 = choix
        elif  pseudo == self.j2.pseudo:
            self.choixJ2 = choix
        else:
            print("partie, setchoix, pas de correspondance de psudo")
    def are2ChoixOK(self):
        """retourne si les 2 joueurs ont fait leur choix"""
        if self.choixJ1 != None and self.choixJ2 != None:
            return True
        else:
            return False