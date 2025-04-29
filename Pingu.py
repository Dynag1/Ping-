# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView, QAbstractItemView, QMessageBox, QMenu
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QAction
from PySide6.QtCore import QObject, Signal, Qt, QPoint, QModelIndex
from src.ui_mainwindow import Ui_MainWindow
from src import var, fct, lic, threadAjIp, threadLancement, db, sFenetre, fctXls
from src.fcy_ping import PingManager
import threading
import qdarktheme
import webbrowser
import importlib



class Communicate(QObject):
    addRow = Signal(str, str, str, str, str, str, bool)
    progress = Signal(int)
    relaodWindow = Signal(bool)

class MainWindow(QMainWindow):
    def closeEvent(self, event):
        # self.ping_manager.stop()  # Ajoutez une méthode stop()
        # self.ping_manager.deleteLater()
        os._exit(0)
        event.accept()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        try:
            theme = db.lire_param_gene()
            qdarktheme.setup_theme(theme[2])
        except:
            qdarktheme.setup_theme("dark")


        self.comm = Communicate()
        self.comm.addRow.connect(self.on_add_row)
        self.comm.progress.connect(self.barProgress)
        self.comm.relaodWindow.connect(self.reload_main_window)
        self.demarre()

    def demarre(self):
        self.ui.labVersion.setText("Ping ü version : "+var.version)
        if lic.verify_license():
            licActive = lic.jours_restants_licence()
            self.ui.labLic.setText("Votre license est active pendant "+licActive+" jours")
        else:
            self.ui.labLic.setText("Vous n'avez pas de license active")
            self.ui.checkMail.setEnabled(False)
            self.ui.checkDbExterne.setEnabled(False)
            self.ui.checkTelegram.setEnabled(False)
            self.ui.checkMailRecap.setEnabled(False)
        self.connector()
        self.plugin = fct.plug(self)
        self.menuPlugin(self.plugin)
        self.ui.progressBar.hide()
        lic.verify_license()
        self.tree_view = self.ui.treeIp
        self.treeIpHeader(self.tree_view)
        self.ui.txtIp.setText(fct.getIp(self))
        self.ui.txtAlive.addItem("Alive")
        self.ui.txtAlive.addItem("Tout")
        self.ui.txtAlive.addItem("Site")
        self.lireParamUi()

    def connector(self):
        self.ui.butIp.clicked.connect(self.butIpClic)
        self.ui.butStart.clicked.connect(self.butStart)
        self.ui.menuClose.triggered.connect(self.close)
        # Modele alertes
        self.ui.spinDelais.valueChanged.connect(self.on_spin_delais_changed)
        self.ui.spinHs.valueChanged.connect(self.on_spin_spinHs_changed)
        self.ui.checkPopup.clicked.connect(self.popup)
        self.ui.checkMail.clicked.connect(self.mail)
        self.ui.checkTelegram.clicked.connect(self.telegram)
        self.ui.checkMailRecap.clicked.connect(self.mailRecap)
        self.ui.checkDbExterne.clicked.connect(self.pingDb)
        # Fentres
        self.ui.actionSauvegarder_les_r_glages.triggered.connect(lambda: self.saveParam)
        self.ui.actionEnvoies.triggered.connect(sFenetre.fenetreParamEnvoie)
        self.ui.actionMail_recap.triggered.connect(sFenetre.fenetreMailRecap)
        self.ui.actionG_n_raux.triggered.connect(lambda: sFenetre.fenetreParametre(self, self.comm))
        # Fonction Save et Load
        self.ui.actionSauvegarder.triggered.connect(lambda: fct.save_csv(self, self.treeIpModel))
        self.ui.actionOuvrir.triggered.connect(lambda: fct.load_csv(self, self.treeIpModel))
        self.ui.actionTout_effacer.triggered.connect(lambda: fct.clear(self, self.treeIpModel))
        # Fonction export excel
        self.ui.actionExporter_xls.triggered.connect(lambda: fctXls.saveExcel(self, self.treeIpModel))
        self.ui.actionImporter_xls.triggered.connect(lambda: fctXls.openExcel(self, self.treeIpModel))

    def menuPlugin(self, plugin):
        for plug in plugin:
            print(plug)
            #self.ui.menuPlugin.addMenu(plug)
            action_directe = QAction(plug, self)
            action_directe.triggered.connect(lambda checked=False, p=plug: self.pluginLance(p))
            # Ajout direct de l'action dans le menu (PAS dans un sous-menu)
            self.ui.menuPlugin.addAction(action_directe)

    def pluginLance(self, plug):
        try:
            # Construction du nom complet du module à importer
            module_name = f"fichier.plugin.{plug}.main"
            plugin_module = importlib.import_module(module_name)
            # Exemple d'utilisation : appel d'une fonction 'run' dans le module
            if hasattr(plugin_module, "main"):
                plugin_module.main(self.comm)
            else:
                print(f"Le plugin '{plug}' n'a pas de fonction 'run'.")
        except Exception as e:
            print(f"Erreur lors du chargement du plugin '{plug}': {e}")

    def lireParamUi(self):
        try:
            variable = db.lire_param_db()
            var.delais = variable[0]
            var.envoie_alert = variable[1]
            print(var.envoie_alert)
            var.popup = variable[2]
            var.mail = variable[3]
            var.telegram = variable[4]
            var.mailRecap = variable[5]
            db.nom_site()
            self.ui.labSite.setText(var.nom_site)
            self.ui.spinDelais.setValue(int(var.delais))
            self.ui.spinHs.setValue(int(var.envoie_alert))
            if var.popup is True:
                self.ui.checkPopup.setChecked(True)
            if var.mail is True:
                self.ui.checkMail.setChecked(True)
            if var.telegram is True:
                self.ui.checkTelegram.setChecked(True)
            if var.mailRecap is True:
                self.ui.checkMailRecap.setChecked(True)
        except Exception as inst:
            print(inst)
        db.creerDossier("bd")
        db.creerDossier("fichier")
        db.creerDossier("fichier/plugin")

    def saveParam(self):
        db.save_param_db()

    def popup(self):
        if self.ui.checkPopup.isChecked():
            var.popup = True
            print(var.popup)
        else:
            var.popup = False
            print(var.popup)

    def mail(self):
        if self.ui.checkMail.isChecked():
            var.mail = True
            print(var.mail)
        else:
            var.mail = False
            print(var.mail)

    def telegram(self):
        if self.ui.checkTelegram.isChecked():
            var.telegram = True
            print(var.telegram)
        else:
            var.telegram = False
            print(var.telegram)

    def mailRecap(self):
        if self.ui.checkMailRecap.isChecked():
            var.mailRecap = True
            print(var.mailRecap)
        else:
            var.mailRecap = False
            print(var.mailRecap)

    def pingDb(self):
        if self.ui.checkDbExterne.isChecked():
            var.dbExterne = True
            print(var.dbExterne)
        else:
            var.dbExterne = False
            print(var.dbExterne)



    def close(self):
        var.tourne = False
        app.aboutToQuit.connect(self.cleanup_threads)
        os._exit(0)

    def treeIpHeader(self, tree_view):
        self.tree_view = self.ui.treeIp
        # Configurer le modèle pour le TreeView
        self.treeIpModel = QStandardItemModel()
        self.treeIpModel.setHorizontalHeaderLabels(["Id", "IP", "Nom", "Mac", "Port", "Latence", "Suivi", "Comm", "Excl"])
        # Appliquer le modèle au TreeView
        self.tree_view.setModel(self.treeIpModel)
        # Configurer l'en-tête horizontal
        header = self.tree_view.header()
        # Désactiver l'étirement automatique de la dernière section
        header.setStretchLastSection(False)
        # Configurer les modes de redimensionnement pour chaque colonne
        for i in range(self.treeIpModel.columnCount()):
            if i in [0, 5, 6, 8]:  # Colonnes figées
                header.setSectionResizeMode(i, QHeaderView.Fixed)
            else:  # Colonnes étirables
                header.setSectionResizeMode(i, QHeaderView.Stretch)
        # Configurer les largeurs initiales des colonnes figées
        self.tree_view.setColumnWidth(0, 1)  # Exemple pour la colonne Id
        self.tree_view.setColumnWidth(5, 50)  # Exemple pour Latence
        self.tree_view.setColumnWidth(6, 50)  # Exemple pour Suivi
        self.tree_view.setColumnWidth(8, 50)  # Exemple pour Excl
        self.tree_view.setStyleSheet("QTreeView, QTreeView::item { color: black; }")
        self.tree_view.setSelectionMode(QAbstractItemView.NoSelection)

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_view.header().setSortIndicator(1, Qt.AscendingOrder)

    def show_context_menu(self, pos: QPoint):
        index = self.tree_view.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu()
        action_web = QAction("Ouvrir dans le navigateur", self)
        action_suppr = QAction("Supprimer", self)
        action_excl = QAction("Exclure", self)
        action_web.triggered.connect(lambda: self.handle_web_action(index))
        action_suppr.triggered.connect(lambda: self.find_and_remove(index))
        action_excl.triggered.connect(lambda: self.ipExcl(index))
        menu.addAction(action_web)
        menu.addAction(action_suppr)
        menu.addAction(action_excl)
        menu.exec(self.tree_view.viewport().mapToGlobal(pos))

    def handle_web_action(self, index: QModelIndex):
        # Accéder aux données via le modèle
        ip_item = self.treeIpModel.item(index.row(), 1)  # Colonne IP
        webbrowser.open('http://' + ip_item.text())
        print(f"Ouverture de {ip_item.text()}")

    def find_and_remove(self, index: QModelIndex):
        self.treeIpModel.removeRow(index.row())

    def ipExcl(self, index: QModelIndex):
        x_item = QStandardItem("x")
        self.treeIpModel.setItem(index.row(), 8, x_item)


    def butIpClic(self):
        ip = self.ui.txtIp.text()
        nbr_hote = self.ui.spinHote.value()
        alive = self.ui.txtAlive.currentText()
        port = self.ui.txtPort.text()
        self.ui.progressBar.show()
        threading.Thread(target=threadAjIp.main, args=(self.comm, self.treeIpModel, ip,nbr_hote, alive, port, "")).start()

    def on_add_row(self, i, ip, nom, mac, port, extra, is_ok):
        items = [
            QStandardItem(i),
            QStandardItem(ip),
            QStandardItem(nom),
            QStandardItem(mac),
            QStandardItem(str(port)),
            QStandardItem(extra),
            QStandardItem(""),
            QStandardItem(""),
            QStandardItem("")
        ]
        if is_ok:
            for item in items:
                item.setBackground(QColor("#1f8137"))
        else:
            for item in items:
                item.setBackground(QColor("#A9A9A9"))
        self.treeIpModel.appendRow(items)

    def butStart(self):
        self.ping_manager = PingManager(self.treeIpModel)
        if self.ui.butStart.isChecked():
            var.tourne = True
            self.ping_manager.start()
            threading.Thread(target=threadLancement.main, args=(self, self.treeIpModel)).start()
        else:
            var.tourne = False
            self.ping_manager.stop()

    def on_spin_delais_changed(self, value):
        var.delais = value
        if value < 60:
            valueA = str(value)+" s"
            valueB = ""
        elif value < 3600:
            valueA = value//60
            valueB = value % 60
            valueB = f"{int(valueB):02d}"
            valueA = str(valueA)+" m "+str(valueB)
        else:
            valueA = value//3600
            valueB = (value % 3600) // 60
            valueA = str(valueA)+" h "+f"{int(valueB):02d}"

        self.ui.labDelaisH.setText(str(valueA))
        print(f"Nouvelle valeur du délai : {var.delais}")

    def on_spin_spinHs_changed(self, value):
        var.nbrHs = value
        print(f"Nouvelle valeur du var.nbrHs : {var.nbrHs}")

    def barProgress(self, i):
        self.ui.progressBar.setValue(i)
        if i == 100:
            self.ui.progressBar.hide()
            QMessageBox.information(
                self,
                "Succès",
                "Scan terminé, "+str(var.u)+" hôtes trouvés",
                QMessageBox.Ok
            )

    def reload_main_window(bool):
        global window
        window.hide()
        window.deleteLater()
        # Recréer la fenêtre
        window = MainWindow()
        window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Créer l'application Qt
    window = MainWindow()         # Instancier la fenêtre principale
    window.show()                 # Afficher la fenêtre principale
    sys.exit(app.exec())         # Exécuter la boucle d'événements
