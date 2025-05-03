# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import time
from datetime import datetime
from src import var, thread_mail, db


def jour_demande():
    jourDemande = tuple()
    data = db.lire_param_mail_recap()
    if data[1]:
        jourDemande = jourDemande + ("0",)
    if data[2]:
        jourDemande = jourDemande + ("1",)
    if data[3]:
        jourDemande = jourDemande + ("2",)
    if data[4]:
        jourDemande = jourDemande + ("3",)
    if data[5]:
        jourDemande = jourDemande + ("4",)
    if data[6]:
        jourDemande = jourDemande + ("5",)
    if data[7]:
        jourDemande = jourDemande + ("6",)
    return jourDemande


def prepaMail(self, tree_model):
    sujet = self.tr("""\
    Compte rendu du site """)+var.nom_site
    message = self.tr("""\
        Bonjour,<br><br>
        Voici le compte rendu des équipements sous surveillance : <br><br>""")


    message = message + self.tr("""<table border="1"><tr><th>Nom</th><th>IP</th><th>Statut</th></tr>""")
    # Parcours du modèle
    for row in range(tree_model.rowCount()):
        index_nom = tree_model.index(row, 2)  # Colonne Nom
        index_ip = tree_model.index(row, 1)   # Colonne IP
        index_statut = tree_model.index(row, 5)  # Colonne Statut

        nom = tree_model.data(index_nom)
        ip = tree_model.data(index_ip)
        statut = tree_model.data(index_statut)

        # Logique de coloration
        color = var.couleur_noir if statut == "HS" else var.couleur_vert

        message += self.tr(f"""
        <tr>
            <td bgcolor="{color}">{nom}</td>
            <td bgcolor="{color}">{ip}</td>
            <td bgcolor="{color}">{statut}</td>
        </tr>""")

    message = message + self.tr("""\
    </table><br><br>
    Cordialement,<br><br>
    <b>PyngOuin<b>
    """)
    try:
        thread_mail.envoie_mail(message, sujet)
    except Exception as inst:
        print(inst)


def main(self, tree_model):
    data = db.lire_param_mail_recap()
    heureDemande = data[0].strftime("%H:%M")
    while True:
        try:
            if var.tourne == 1:
                if var.mailRecap == 1:
                    a = False
                    j = jour_demande()
                    d = datetime.now()
                    jour = str(d.weekday())
                    heure = d.strftime('%H:%M')
                    for x in j:
                        print(x)
                        if str(x) == jour:
                            if str(heure) == str(heureDemande):
                                a = True
                    if a is True:
                        prepaMail(self, tree_model)
                    time.sleep(60)
                else:
                    break
            else:
                break
        except Exception as inst:
            print("thread_recap - " + str(inst))
