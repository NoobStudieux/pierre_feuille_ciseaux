
import threading
from tkinter import *

class ThreadReception(threading.Thread):
    def __init__(self,connexion, fenetre):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.fenetre = fenetre
    def run(self):
        while True:
            message = self.connexion.recv(1024).decode("Utf8")
            print(message)
            if message.split(", ")[1] == "listeConnectes":
                # nettoyage
                for widget in self.fenetre.connectes.winfo_children():
                    widget.destroy()
                # ré-édition
                for i in range(2,len(message.split(", "))):
                    if message.split(", ")[i] != self.fenetre.pseudo:
                        l = Label(self.fenetre.connectes, text=message.split(", ")[i])
                        l.bind("<Button-1>", lambda event, x = message.split(", ")[i] :self.clickPseudo(x))
                        l.pack()
            elif message.split(", ")[1] == "vousEtesDeco":
                break
            elif message.split(", ")[1] == "nouvellePartie":
                adversaire = ""
                if self.fenetre.pseudo == message.split(", ")[2]:
                    adversaire = message.split(", ")[3]
                elif self.fenetre.pseudo == message.split(", ")[3]:
                    adversaire = message.split(", ")[2]
                else:
                    print("erreur bizarre n°89")
                    adversaire = "inconnu"
                
                self.bouton_pierre = Button(self.fenetre.jeu, text="pierre", command=self.choixPierre)
                self.bouton_feuille = Button(self.fenetre.jeu, text="feuille", command=self.choixFeuille)
                self.bouton_ciseaux = Button(self.fenetre.jeu, text="ciseaux", command=self.choixCiseaux)
                self.bouton_valider_choix = Button(self.fenetre.jeu, text="valider", command=self.validerChoix)
                self.bouton_pierre.pack(side=LEFT)
                self.bouton_feuille.pack(side=LEFT)
                self.bouton_ciseaux.pack(side=LEFT)
                self.bouton_valider_choix.pack(side=BOTTOM)
                Label(self.fenetre.jeu, text ="vous jouez contre " + str(adversaire)).pack(side=BOTTOM)   
    def clickPseudo(self, partenaire):
        print(partenaire)
        message = self.fenetre.pseudo + ", demandePartie, " + partenaire
        self.connexion.send(message.encode("Utf8"))
    def choixPierre(self):
        self.fenetre.choix = "pierre"
    def choixFeuille(self):
        self.fenetre.choix = "feuille"
    def choixCiseaux(self):
        self.fenetre.choix = "ciseaux"
    def validerChoix(self):
        if self.fenetre.choix == "":
            print("vous devez choisir une action avant") # afficher en fenetre ?
        else:
            message = self.fenetre.pseudo + ", partieEnCours, choix, " + self.fenetre.choix
            self.connexion.send(message.encode("utf8"))
