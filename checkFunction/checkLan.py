from base64 import decode, encode
from cmath import e
from email import header
import socket
import subprocess
import netifaces
import telnetlib
import re
import PySimpleGUI as sg
import os
from scapy.all import ARP,Ether,srp
import time

USER = open("./checkFunction/usr.lst").read().splitlines()
PASS = open("./checkFunction/pass.lst").read().splitlines()
IP = ""
MAC = ""
SCAN = ""
NMAP = ""
SSH = ""


# IPを取得


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# デフォルトゲートウェイを取得


def getGatewayIP():
    gw = netifaces.gateways()
    return gw["default"][2][0] + "/24"

# 無線LAN情報の表示


def checkLan():
    rec = subprocess.run(
        ["sudo","wpa_cli","-i" ,"wlx1cc03504484f" ,"status"], capture_output=True)
    return rec.stdout.decode("cp932")

# 無線LANに接続されている機器の表示

def network_scanner():
    global SCAN
    rec = ""
    clients = []
    target_IP = getGatewayIP()
    #create ARP packets
    arp = ARP(pdst=target_IP)
    #create the Ether bradcast packets
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    #stack them
    packet = ether/arp
    result = srp(packet,timeout=3)[0]
    for sent,received in result:
        clients.append({"ip":received.psrc,"mac":received.hwsrc})
    #print clients
    for client in clients:
        rec += "{:16}    {}".format(client["ip"],client["mac"]) + "\n"
    SCAN = "無線LAN内の機器\n" + "IP" + " "*28+"MAC\n"+ rec
    return SCAN


def scan():
    pas = "kali\n".encode()
    rec = subprocess.run([
         "sudo" ,"nmap", "-sP", getGatewayIP()], capture_output=True,input=pas)
    global NMAP 
    NMAP = rec.stdout.decode("cp932")
    return rec.stdout.decode("cp932")

# 無線LANの暗号化規格の確認


def checkCrypted():
    if "WPA2" in checkLan():
        return "無線LANルーターの暗号化規格:WPA2\nお使いの無線LANルーターは安全な暗号化規格です"
    elif "WPA" in checkLan():
        return "....ok"
    else:
        return "ng"

# 入力したIPアドレスのポートスキャン


def portScan(ip):
    rec = subprocess.run(["sudo", "nmap", ip], capture_output=True)
    return rec.stdout.decode("cp932")


def extractIP():
    ip = re.findall(
        "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", SCAN)
    if getIP() in IP:
        IP.remove(getIP())
    return ip


def extractMAC():
    mac = re.findall(
        "(?:[0-9a-fA-F]:?){12}", SCAN)
    return mac


def extractVender():
    rec = subprocess.run([],capture_output=True)
    
def is_ssh_open(ip):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = sock.connect_ex((ip,22))
    if result == 0:
        return True,"△"
    else:
        return False,"○"

def ssh_open(ip):
    pass


def is_telnet_open(ip):
    rec = False
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = sock.connect_ex((ip,23))
    if result == 0:
        return True,"△"
    else:
        return False,"○"


def ssh_Crack(ip):
    flag = False
    rec = subprocess.run(["hydra","-L","./checkFunction/usr.lst","-P","./checkFunction/pass.lst","-t","4",ip,"ssh"],capture_output=True)
    target_IP_Scan =  rec.stdout.decode("cp932")
    if "successfully completed" in target_IP_Scan:
        flag = True
    return flag
            

def telnet_Crack(ip):
    flag = False
    rec = subprocess.run(["hydra","-L","./checkFunction/usr.lst","-P","./checkFunction/pass.lst","-t","4",ip,"telnet"],capture_output=True)
    target_IP_Scan =  rec.stdout.decode("cp932")
    if "successfully completed" in target_IP_Scan:
        flag = True
    return flag
            
# def ssh_check():
#     target_IP = extractIP()
#     rec = ""
#     for ip in target_IP:
#         if is_ssh_open(ip):
#             if ssh_Crack(ip):
#                 rec += ip     
#     return rec


# def telnet_check():
#     target_IP = extractIP()
#     rec = ""
#     for ip in target_IP:
#         if is_telnet_open(ip):
#             if telnet_Crack(ip):
#                 rec += ip
#     return rec

def ssh_check(ip):
    rec = ""
    if is_ssh_open(ip)[0]:
        if ssh_Crack(ip):
            rec += ip
            return "×"
        else:
            return "○"
    else:
        return "○"

def telnet_check(ip):
    rec = ""
    if is_telnet_open(ip)[0]:
        if telnet_Crack(ip):
            rec += ip
            return "×"
        else:
            return "○"
    else:
        return "○"

            
def vulnerabilityResult(): 
    # rec = "IP" + " "*27+"MAC" + " "*33 + "ssh_open" + " "*5 + "ssh_pass" + " "*5 + "telnet_open" + " "*5 + "telnet_pass" + "\n"
    # for ip ,mac in zip(extractIP(),extractMAC()):
    #     rec += "{:16}    {}".format(ip,mac) +  " "*6  + is_ssh_open(ip)[1] + " "*20 + ssh_check(ip) + " "*18 + is_telnet_open(ip)[1] + " "*24 + telnet_check(ip) + "\n"
    # return rec
    a = [[]]
    b = []
    for ip ,mac in zip(extractIP(),extractMAC()):
        #a.extend([ip,mac,is_ssh_open(ip)[1],ssh_check(ip),is_telnet_open(ip)[1],telnet_check(ip)])
        b = [ip,mac,is_ssh_open(ip)[1],ssh_check(ip),is_telnet_open(ip)[1],telnet_check(ip)]
        a.append(b)
    
    return a



    #rec = f"ssh open : {ssh_check()}\ntelnet open : {telnet_check()}"
    #return network_scanner()


def krack_script(target_mac):
    rec = ""
    os.chdir("./krackattacks-scripts/krackattack")
    try:
        rec = subprocess.run(["./krack-test-client.py"],timeout=70,capture_output=True)
    except subprocess.TimeoutExpired:
        return rec

