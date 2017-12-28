
import threading, socket, sys, time
import ressources_serveur.Joueur as joueur 
import ressources_serveur.Partie as partie

class ThreadEnvoiListeConnectes(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            if len(conn_client)>0:
                message = "serveur, listeConnectes"
            # composition du message
                for c in conn_client:
                    message += ", " + conn_client[c]['joueur'].pseudo
            # envoi du message à chaque connectes
                for c in conn_client:
                    conn_client[c]['connexion'].send(message.encode("Utf8"))
            time.sleep(5)

class ThreadClient(threading.Thread):
    def __init__(self, connexion):
        threading.Thread.__init__(self)
        self.connexion = connexion
    def run(self):
        while True:
            messClient = self.connexion.recv(1024).decode("Utf8")
            print(messClient)
            if messClient.split(', ')[1] == 'pseudo':
                conn_client[self.getName()]['joueur'].setPseudo(messClient.split(', ')[2])
            elif messClient.split(', ')[1] == 'jemedeco':
                print("jemedeco -  ", messClient.split(', ')[0])
                message = "serveur, vousEtesDeco"
                conn_client[self.getName()]['connexion'].send(message.encode("Utf8"))
                break
            elif messClient.split(', ')[1] == "demandePartie":
                message = "serveur, nouvellePartie, " + messClient.split(', ')[0] + ", " + messClient.split(', ')[2]
                if not self.isEnTrainDeJouer(messClient.split(', ')[0]) and not  self.isEnTrainDeJouer(messClient.split(', ')[2]):
                    parties.append(partie.Partie(self.getJoueurFromPseudo(messClient.split(', ')[0]), self.getJoueurFromPseudo(messClient.split(', ')[2]) ))
                    self.envoiMessageAUnPseudo(messClient.split(', ')[0] , message)
                    self.setEnTrainDeJouer(messClient.split(', ')[0])
                    self.envoiMessageAUnPseudo(messClient.split(', ')[2] , message)
                    self.setEnTrainDeJouer(messClient.split(', ')[2])
            elif messClient.split(', ')[1] == "partieEnCours": # <pseudo>, partieEnCours, <option>, <valeur>
                if messClient.split(', ')[2] == "choix":
                    partie_courante = self.getPartieFromPseudo(messClient.split(', ')[0])
                    partie_courante.setChoix(messClient.split(', ')[0], messClient.split(', ')[3])
                    if partie_courante.are2ChoixOK(): # les 2 joueurs ont fait leur choix
                        partie_courante.concourir()
                        message = "serveur, vainqueur, " + partie_courante.gagnant
                        self.envoiMessageAUnPseudo(partie_courante.j1.pseudo , message)
                        self.envoiMessageAUnPseudo(partie_courante.j2.pseudo , message)
            elif messClient.split(', ')[1] == "rejouer":
                self.setDispo(messClient.split(', ')[0])
        print("deconnexion de " , self.getName(), " (", conn_client[self.getName()]['joueur'].pseudo , ")")
        del conn_client[self.getName()]
    def getJoueurFromPseudo(self, pseudo):
        for c in conn_client:
            if conn_client[c]['joueur'].pseudo == pseudo:
                return conn_client[c]['joueur']
    def getNomThreadFromPseudo(self, pseudo):
        for c in conn_client:
            if conn_client[c]['joueur'].pseudo == pseudo:
                return c
    def getPartieFromPseudo(self, pseudo):
        for p in parties:
            if p.j1.pseudo == pseudo or p.j2.pseudo == pseudo:
                return p
    def envoiMessageAUnPseudo(self, pseudo, message):
        for c in conn_client:
            if conn_client[c]['joueur'].pseudo == pseudo:
                conn_client[c]['connexion'].send(message.encode('Utf8'))
    def isEnTrainDeJouer(self, pseudo):
        for c in conn_client:
            if conn_client[c]['joueur'].pseudo == pseudo:
                return conn_client[c]['joueur'].enCoursDePartie
    def setEnTrainDeJouer(self, pseudo):
        for c in conn_client:
            if conn_client[c]['joueur'].pseudo == pseudo:
                conn_client[c]['joueur'].setEnCoursDePartie()
    def setDispo(self, pseudo):
        for c in conn_client:
            if conn_client[c]['joueur'].pseudo == pseudo:
                conn_client[c]['joueur'].setJoueurDispo()


        
HOST = '127.0.0.1'
PORT = 50000
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a echoué")
    sys.exit()
print("serveur prêt, en attente de requêtes")
mySocket.listen(5)

conn_client = {}
parties=[]
telc = ThreadEnvoiListeConnectes()
telc.start()
while True:
    """boucle et attend un nouveau client à chaque cycle"""
    connexion, adresse = mySocket.accept()
    
    th = ThreadClient(connexion)
    it = th.getName() # identifiant du thread
    conn_client[it] = {'connexion':connexion, 'joueur': joueur.Joueur(it)}
    th.start()
    it = th.getName() # identifiant du thread
    conn_client[it] = {'connexion':connexion, 'joueur': joueur.Joueur(it)}
    print(it)
    print(conn_client[it]['joueur'].nom_thread)
    print("Client %s connecté, adresse IP %s, port %s."% (it, adresse[0], adresse[1]))