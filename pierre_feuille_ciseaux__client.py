
import threading, socket, sys
from tkinter import *

import ressources_client.Fenetre as fen

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 50000
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host,port))
    except socket.error:
        print("la connexion a echoue")		
        sys.exit()
    print("connexion établie avec le serveur")

    fen.Fenetre(connexion).mainloop()
