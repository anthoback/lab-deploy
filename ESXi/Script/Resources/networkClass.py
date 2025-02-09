
import os 

from Resources.samples import *



class network:
    # Est lié à un lab, permet de gérer tous les aspects liés au réseau
    def __init__(self,labname:str):
        self.name = ""
        self.IPmask = ""
        self.labname=labname
        self.getHostOnlyNetwork()
        self.getIPmask()
    
    def ESXiCmd(self, command:str):
        # Exécute une commande sur l'ESXi, utilisée partout
        print(os.getenv('user') + "@" + os.getenv('ESXi') + " " + command)
        os.chdir("..")
        os.system("sshpass -p " + os.getenv('password') + " ssh -o StrictHostKeyChecking=no " + os.getenv('user') + "@" + os.getenv('ESXi') + " " + command)
        os.chdir("Script")
    
    def getHostOnlyNetwork(self):
        # Chosit un des réseaux disponibles dans Networks.txt
        # pour en ajouter un il faut l'ajouter sur l'ESXi , y connecter le pfsense et configure le pare-feu de ce dernier pour donner l'accès à internet
        fichier = open("Resources/Networks.txt", 'r')
        liste = fichier.readlines()
        fichier.close()
        for i in range(len(liste)):
            opts = liste[i].split(" ")
            host_id = opts[0].replace("HostOnly", "")
            lab_id = self.labname.replace("Lab", "")
            if opts[1] == "unused" and host_id == lab_id:
                liste[i] = opts[0] + " used " + opts [2]
                fichier = open("Resources/Networks.txt", 'w')
                fichier.writelines(liste)
                fichier.close()
                self.name = opts[0]
                self.IPmask = opts[2].replace("\n", "")
                return 
        print("No free HostOnly network with this number, please create or free the appropriate one")
        exit(1)

    def getIPmask(self):
        fichier = open("Resources/Networks.txt", 'r')
        liste = fichier.readlines()
        fichier.close()
        for i in range(len(liste)):
            opts = liste[i].split(" ")
            host_id = opts[0].replace("HostOnly", "")
            lab_id = self.labname.replace("Lab", "")
            if host_id == lab_id:
                self.IPmask = opts[2].replace("\n", "")
                return opts[2].replace("\n", "")
        print("No free HostOnly network with this number, please create or free the appropriate one")
        exit(1)

    def freeHostOnlyNetwork(self):
        # Inverse de la fonction précédente.
        fichier = open("Resources/Networks.txt", 'r')
        liste = fichier.readlines()
        fichier.close()
        for i in range(len(liste)):
            opts = liste[i].split(" ")
            if opts[0] == self.name:
                liste[i] = opts[0] + " unused " + opts[2]
                fichier = open("Resources/Networks.txt", 'w')
                fichier.writelines(liste)
                fichier.close()
                return 
        print("Network to be freed not found !")
        exit(1)