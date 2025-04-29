# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import src.db as param_mail
from email.utils import formatdate


def envoie_mail(messageRecep, sujet):
    variables = param_mail.lire_param_mail()

    destinateur = variables[0]
    password = variables[1]
    port = variables[2]
    smtp_server = variables[3]
    destinataire = variables[4]
    message = MIMEMultipart('alternative')
    message['Subject'] = sujet
    message['From'] = destinateur
    message['To'] = destinataire
    message['Date'] = formatdate(localtime=True)

    email_texte = messageRecep
    email_html = messageRecep

    mimetext_texte = MIMEText(email_texte, "texte")
    mimetext_html = MIMEText(email_html, "html")
    message.attach(mimetext_texte)
    message.attach(mimetext_html)
    try:
        context = ssl.create_default_context()
    except Exception as inst:
        print("fct_tread_mail"+inst)
        return
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(destinateur, password)
            try:
                server.sendmail(destinateur, destinataire.split(","), message.as_string())
            except Exception as inst:
                print("fct_tread_mail" + inst)
            server.quit()
            print("Test envoie mail OK")
    except Exception as inst:
        print("fct_tread_mail"+inst)

