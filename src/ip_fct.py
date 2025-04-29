
# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import socket
from contextlib import closing
import time
import platform
import os, sys
import pythonping

#############################################################################################
#####	Récupérer les adresses MAC														#####
#############################################################################################
def getmac(ip):
        mac = ""
        try:
                my_os = platform.system()
                if my_os == "Windows":
                        # grep with a space at the end of IP address to make sure you get a single line
                        fields = os.popen('arp -a ' + ip).read().split()
                        if len(fields) == 12 and fields[10] != "00:00:00:00:00:00":
                                mac = fields[10]
        except Exception as e:
                print(str(e))
                pass
        return mac

#############################################################################################
#####	Tester les ports ouvert															#####
#############################################################################################
def check_port(host,port):
        result = ""
        try:
                if len(port) > 0:
                        port01 = port.split(",")
                        for port02 in port01:
                                result = result + check_socket(host, port02)
        except Exception as e:
                print(str(e))
                pass
        return result

#############################################################################################
#####	Récupérer les Noms																#####
#############################################################################################
def check_socket(host, port):
        try:
                with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                        if sock.connect_ex((host, int(port))) == 0:
                                return str(port)+"/"
                        else:
                                return ""
        except Exception as e:
                print(str(e))
                return ""

#############################################################################################
#####	Effectuer un ping																#####
#############################################################################################
def ipPing(ip):
        try:
                result = pythonping.ping(ip, size=10, count=1)
                if result.rtt_avg_ms == int(2000):
                        return "HS"
                else:
                        return "OK"

        except Exception as inst:
                print(inst)

#############################################################################################
#####	Récupérer l'adresse ip.pin															#####
#############################################################################################
def recup_ip():
        try:
                h_name = socket.gethostname()
                IP_addres = socket.gethostbyname(h_name)
                ip = IP_addres.split(".")
                ipadress = ip[0]+"."+ip[1]+"."+ip[2]+".1"
                return ipadress
        except Exception as e:
                print(str(e))
