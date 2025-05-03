from src import var
import pickle
import os.path
from pathlib import Path
from PySide6.QtCore import Qt


"""**************
    Creer dossier
**************"""
fichierini = "tabG"


def creerDossier(nom):
    # Spécifiez le chemin du dossier à créer
    chemin_dossier = os.getcwd()+"\\"+nom

    # Vérifiez si le dossier n'existe pas, puis créez-le
    dossier = Path(chemin_dossier)
    if not dossier.exists():
        dossier.mkdir(parents=True, exist_ok=True)
    else:
        pass


def lireNom(ip, model):
    # Parcourir toutes les lignes
    for row in range(model.rowCount()):
        index_ip = model.index(row, 1)  # Colonne 0 = IP
        # Vérifier le match d'IP
        if model.data(index_ip, Qt.DisplayRole) == ip:
            # Récupérer colonne 3 (index 2)
            index_col3 = model.index(row, 2)
            print(ip)
            return model.data(index_col3, Qt.DisplayRole)
    return None  # Si non trouvé


"""***************
    Param Géné
***************"""


def nom_site():
    try:
        param = lire_param_gene()
        var.nom_site = param[0]
        var.l = param[1]
    except Exception as inst:
        print("param_gene - "+str(inst))
        return param[0]


def lire_param_gene():
    try:
        if os.path.isfile(fichierini):
            fichierSauvegarde = open(fichierini, "rb")
            variables = pickle.load(fichierSauvegarde)
            fichierSauvegarde.close()
            return variables
        else:
            print("Fichier " + fichierini + " non trouvé")
    except Exception as inst:
        print("param_gene - "+str(inst))


def save_param_gene(param_site, param_li, param_theme):
    variables = [param_site, param_li, param_theme]
    try:
        fichierSauvegarde = open(fichierini, "wb")
        pickle.dump(variables, fichierSauvegarde)
        fichierSauvegarde.close()
    except Exception as inst:
        print("param_gene - "+str(inst))


"""**************
    DB Param
**************"""


def lire_param_db():
    try:
        fichierini = "tab4"
        if os.path.isfile(fichierini):
            fichierSauvegarde = open(fichierini, "rb")
            variables = pickle.load(fichierSauvegarde)
            fichierSauvegarde.close()
            return variables
        else:
            print("Fichier "+fichierini+" non trouvé")
    except Exception as inst:
        print(inst)


def save_param_db():
    try:
        param_delais = var.delais
        param_nbr_hs = var.nbrHs
        param_popup = var.popup
        param_mail = var.mail
        param_telegram = var.telegram
        param_mail_recap = var.mailRecap
        param_db_ext = var.dbExterne
        variables = [param_delais, param_nbr_hs, param_popup, param_mail, param_telegram, param_mail_recap, param_db_ext]
        try:
            fichierSauvegarde = open("tab4", "wb")
            pickle.dump(variables, fichierSauvegarde)
            fichierSauvegarde.close()
        except Exception as inst:
            print((inst))
            return
    except Exception as inst:
        print((inst))


"""**************
    DB Param Mail
**************"""


def lire_param_mail():
    fichierini = "tab"
    try:
        if os.path.isfile(fichierini):
            fichierSauvegarde = open(fichierini, "rb")
            variables = pickle.load(fichierSauvegarde)
            fichierSauvegarde.close()
            return variables
        else:
            return False
            print("Fichier " + fichierini + " non trouvé")
    except Exception as inst:
        print(inst)


def save_param_mail(variables):
    try:
        fichierSauvegarde = open("tab", "wb")
        pickle.dump(variables, fichierSauvegarde)
        fichierSauvegarde.close()
    except Exception as inst:
        print(inst)
    return


"""***********************
    Parametres mail recap
**********************"""


def save_param_mail_recap(value):
    try:
        fichierSauvegarde = open("tabr","wb")
        pickle.dump(value, fichierSauvegarde)
        fichierSauvegarde.close()
    except Exception as inst:
        print("mail-"+str(inst))
        return


def lire_param_mail_recap():
    fichierini = "tabr"
    try:
        if os.path.isfile(fichierini):
            fichierSauvegarde = open(fichierini, "rb")
            variables = pickle.load(fichierSauvegarde)
            fichierSauvegarde.close()

            # Affichage de la liste
            return variables
        else:
            # Le fichier n'existe pas
            print("Fichier " + fichierini + " non trouvé")
    except Exception as inst:
        print("mail-"+str(inst))
