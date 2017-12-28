#!/usr/bin/python3.6
#-*-coding=Utf8-*-
from tkinter import *
import ressources_client.Threads as thr

import os
class Fenetre(Frame):
    def __init__(self, connexion):
        Frame.__init__(self, height=400, width=400)
        self.connexion = connexion
        self.label1 = Label(self, text="votre pseudo : ")
        self.label1.pack()
        self.saisie_pseudo = Entry(self)
        self.saisie_pseudo.pack()
        self.valider_pseudo = Button(self, text="valider", command=self.validerPseudo)
        self.valider_pseudo.pack()
        self.pseudo = ""
        self.choix = ""  # pierre, feuille ou ciseaux
        self.boutonQuitter = Button(self, text="quitter", command=self.destruction)
        self.boutonQuitter.pack()
        self.connectes = Frame(self)
        self.connectes.pack(side=LEFT)
        self.jeu = Frame(self)
        self.jeu.pack(side=RIGHT)
        self.pack()
    def destruction(self):
        print("destruction fenêtre")
        message = self.pseudo  + ", jemedeco"
        self.connexion.send(message.encode("Utf8"))
        self.destroy()
    def validerPseudo(self):
        tr = thr.ThreadReception(self.connexion, self)
        tr.start()
        self.pseudo = self.saisie_pseudo.get()
        message = self.pseudo + ", pseudo, " + self.pseudo
        self.connexion.send(message.encode("Utf8"))
        self.saisie_pseudo.pack_forget()
        self.valider_pseudo.pack_forget()
        self.label1.pack_forget()