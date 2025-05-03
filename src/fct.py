# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import socket
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QAbstractItemModel, QModelIndex
from PySide6.QtGui import QStandardItem, QStandardItemModel
import csv
import os
import sys


def getIp(self):
    try:
        h_name = socket.gethostname()
        IP_addres = socket.gethostbyname(h_name)
        ip = IP_addres.split(".")
        ipadress = ip[0]+"."+ip[1]+"."+ip[2]+".1"
        return ipadress
    except Exception as e:
        print("fct_ip - " + str(e))


def save_csv(self, treeModel):
    try:
        # Récupérer le modèle depuis le QTreeView
        model = treeModel

        if not isinstance(model, QAbstractItemModel):
            raise ValueError("Modèle invalide - doit hériter de QAbstractItemModel")

        # Boîte de dialogue de sauvegarde Qt
        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr("Enregistrer le fichier"),
            dir=os.getcwd() + os.sep + "bd",
            filter=self.tr("Fichiers PIN (*.pin);;Tous fichiers (*.*)")
        )

        if not filename:
            return

        # Forcer l'extension .pin si non précisée
        if not filename.lower().endswith('.pin'):
            filename += '.pin'

        with open(filename, 'w', newline='', encoding='utf-8') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')

            # Parcourir les lignes du modèle
            for row in range(model.rowCount()):
                row_data = []
                for column in range(model.columnCount()):
                    index = model.index(row, column)
                    row_data.append(model.data(index))
                csvwriter.writerow(row_data)

        # Lancer l'alerte dans un thread séparé
        QMessageBox.information(
            self,
            self.tr("Succès"),
            self.tr("Données sauvegardés"),
            QMessageBox.Ok
        )
    except Exception as e:
        print("design - " + str(e))
        return


def load_csv(self, treeModel):
    try:
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption=self.tr("Ouvrir un fichier"),
            dir=os.getcwd() + os.sep + "bd",
            filter=self.tr("Fichiers PIN (*.pin);;Tous fichiers (*.*)")
        )

        if not filename:
            return

        # Sauvegarde des en-têtes existants
        headers = [treeModel.horizontalHeaderItem(i).text()
                  for i in range(treeModel.columnCount())] if treeModel.columnCount() > 0 else []

        with open(filename, 'r', encoding='utf-8') as myfile:
            csvread = csv.reader(myfile, delimiter=',')

            # Réinitialisation propre
            treeModel.removeRows(0, treeModel.rowCount())  # Conserve les en-têtes

            for row in csvread:
                items = [QStandardItem(str(field)) for field in row]
                treeModel.appendRow(items)

            # Réapplication des en-têtes si nécessaire
            if headers and treeModel.columnCount() == 0:
                treeModel.setHorizontalHeaderLabels(headers)

        QMessageBox.information(self, self.tr("Succès"), self.tr("Données chargées avec succès"), QMessageBox.Ok)

    except Exception as e:
        QMessageBox.critical(self, self.tr("Erreur"), f"Erreur lors du chargement : {str(e)}", QMessageBox.Ok)



def clear(self, treeModel):
    treeModel.removeRows(0, treeModel.rowCount())


def add_row(self, model, row_data):
    """Ajoute une ligne selon le type de modèle"""
    if isinstance(model, QStandardItemModel):
        # Version pour QStandardItemModel
        items = [QStandardItem(str(field)) for field in row_data]
        model.appendRow(items)

    elif hasattr(model, 'add_data'):
        # Version pour modèle personnalisé
        model.add_data(row_data)

    elif hasattr(model, '_data'):
        # Fallback pour modèle basique
        model._data.append(row_data)
        if hasattr(model, 'dataChanged'):
            top_left = model.index(len(model._data)-1, 0)
            bottom_right = model.index(len(model._data)-1, len(row_data)-1)
            model.dataChanged.emit(top_left, bottom_right)


def plug(self):
    # Chemin du dossier 'fichier' situé à côté du script
    script_principal_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Chemin complet du dossier cible (avec sous-dossier 'plugin')
    dossier_fichier = os.path.join(script_principal_dir, 'fichier', 'plugin')

    # Création récursive des dossiers (ne fait rien s'ils existent déjà)
    os.makedirs(dossier_fichier, exist_ok=True)

    # Lister le contenu (uniquement après création du dossier)
    try:
        elements = os.listdir(dossier_fichier)
    except FileNotFoundError:  # Redondant avec makedirs mais sécurisé
        return []

    # Filtrer les sous-dossiers
    sous_dossiers = [
        nom for nom in elements
        if os.path.isdir(os.path.join(dossier_fichier, nom))
    ]

    return sous_dossiers
