# This Python file uses the following encoding: utf-8
from ui_mainwindow import Ui_MainWindow
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QObject

class DataSender(QObject):
    # data_ready = pyqtSignal(str)  # Signal émettant une chaîne de caractères

    def send_data(self, data):
        self.data_ready.emit(data)  # Émettre le signal avec les données

def test():
    row_data = [
                QStandardItem("1"),                # Id
                QStandardItem("ip"),      # IP
                QStandardItem("Nom de l'hôte"),    # Nom
                QStandardItem("00:1A:2B:3C:4D:5E"),# Mac
                QStandardItem("8080"),             # Port
                QStandardItem("20ms"),             # Latence
                QStandardItem("Oui"),              # Suivi
                QStandardItem("Commentaire"),      # Comm
                QStandardItem("Non")               # Excl
            ]
    for item in row_data:
                item.setEditable(True)  # Permettre la modification des cellules

    Ui_MainWindow.treeIpModel.appendRow(row_data)
    row_data2 = [
                QStandardItem("2"),                # Id
                QStandardItem("ip2"),      # IP
                QStandardItem("Nom de l'hôte"),    # Nom
                QStandardItem("00:1A:2B:3C:4D:5E"),# Mac
                QStandardItem("8080"),             # Port
                QStandardItem("20ms"),             # Latence
                QStandardItem("Oui"),              # Suivi
                QStandardItem("Commentaire"),      # Comm
                QStandardItem("Non")               # Excl
            ]
    for item in row_data2:
                item.setEditable(True)  # Permettre la modification des cellules

    Ui_MainWindow.treeIpModel.appendRow(row_data2)
