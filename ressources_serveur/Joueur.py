#!/usr/bin/python3.6
#-*-coding=Utf8-*-

class Joueur:
    def __init__(self, nom_thread, pseudo=""):
        self.nom_thread = nom_thread
        self.pseudo = pseudo
        self.enCoursDePartie = False
    def setPseudo(self, pseudo):
        self.pseudo = pseudo
    def setEnCoursDePartie(self):
        self.enCoursDePartie = True
    def setJoueurDispo(self):
        self.enCoursDePartie = False