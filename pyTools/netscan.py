#Herramientas externas
import scapy.all as scapy
import re
import subprocess
#Visual imports
from progress.bar import ChargingBar
from simple_term_menu import TerminalMenu as tmenu

# TABLA DE REFERENCIA A LOS MENUS
#  -1 = <---
#   0 = Menu inicial
#   1 = Menu Targeta de red
#   2 = Menu de Timeout
#   3 = Scan mode
def menu(menuid):
    m0 = ["My info","ARP --> IP to get MAC","<EXIT>"]
    m1 = ""#get_interfaces()
    m2 = ["Rapidisimo (Nada fiable)","Rapido (No muy fiable)", "Media (Con fallos)","Lento (Fiable)","Muy lento (Muy Fiable)","<---"]
    m3 = ["Scan 1x1 all net", "Scan ip manual","<---"]
    menus = {-1:"<---",0:m0, 1:m1, 2:m2, 3:m3}
    terminal_menu = tmenu(menus[menuid])
    menu_entry_index = terminal_menu.show()
    return menu_entry_index

def get_info(interface):
    try:
        ifconfig_output = subprocess.check_output(["ifconfig", interface])
    except:
        # UnboundLocalError
        # IndexError
        print("[-] La tarjeta de red introducida no existe")
    re_output = re.findall(
        r"(25[0-5]|2[0-4][0-9]|[1-2]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\W(25[0-5]|2[0-4][0-9]|[1-2]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\W(25[0-5]|2[0-4][0-9]|[1-2]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0).(25[0-5]|2[0-4][0-9]|[1-2]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])", str(ifconfig_output))
    waste_myip = re_output[0]
    waste_masc = re_output[1]
    myip = (f"{waste_myip[0]}.{waste_myip[1]}.{waste_myip[2]}.{waste_myip[3]}")
    masc = (f"{waste_masc[0]}.{waste_masc[1]}.{waste_masc[2]}.{waste_masc[3]}")

    # ipxarxa
    ipxarxa = [0, 0, 0, 0]
    bipx = ""
    # bucle que calcula la ip de red por partes
    npart = 0
    while npart <= 3:
        # traducir la seccion a binario
        bmascpart = bin(int(waste_masc[npart]))
        bippart = bin(int(waste_myip[npart]))
        # Corrige el binario en caso de haver omitido los 0's de la izquierda
        if len(bippart) != 10:
            bippart = bippart[0:2] + ("0" * (10 - len(bippart))) + bippart[2:]
        z = 2
        # Atajo para cuando la sección de la mascara es 255
        if str(bmascpart[-1]) == "1":
            ipxarxa[npart] = int(waste_myip[npart])
        # Atajo para cuando la sección de la mascara es 0
        elif str(bmascpart[2]) == "0":
            ipxarxa[npart] = 0
        else:
            # Bucle para hacer el and con el binario i guardarlo en la variable bipx
            while z <= int(len(bmascpart))-1:
                bipx = bipx + str(int(bippart[z]) * int(bmascpart[z]))
                z = z + 1
            bipx = "0b"+bipx
            ipxarxa[npart] = int(ipxarxa[npart] + int(bipx, 2))
        npart = npart + 1
    ipx = (f"{ipxarxa[0]}.{ipxarxa[1]}.{ipxarxa[2]}.{ipxarxa[3]}")
    intipx = [int(ipxarxa[0]), int(ipxarxa[1]),
              int(ipxarxa[2]), int(ipxarxa[3])]
    gw = (f"{ipxarxa[0]}.{ipxarxa[1]}.{ipxarxa[2]}.{ipxarxa[3]+1}")

    # ipbroad
    ipbroad = [0, 0, 0, 0]
    bipbroad = ""
    # calculo de ip broadcast de la xarxa per parts
    npart = 0
    while npart <= 3:
        bmascpart = bin(int(waste_masc[npart]))
        bippart = bin(int(waste_myip[npart]))
        if len(bippart) != 10:
            bippart = bippart[0:2] + ("0" * (10 - len(bippart))) + bippart[2:]
        z = 2
        if str(bmascpart[-1]) == "1":
            ipbroad[npart] = int(waste_myip[npart])
        elif str(bmascpart[2]) == "0":
            ipbroad[npart] = 255
        else:
            while z <= int(len(bmascpart))-1:
                if bmascpart[z] == "1":
                    bipbroad = bipbroad + bippart[z]
                else:
                    bipbroad = bipbroad + "1"
                z = z + 1
            bipbroad = "0b"+bipbroad
            ipbroad[npart] = int(ipbroad[npart] + int(bipbroad, 2))
        npart = npart + 1
    bro = (f"{ipbroad[0]}.{ipbroad[1]}.{ipbroad[2]}.{ipbroad[3]}")

    # transformo la mascara a enteros
    intmasc = [int(waste_masc[0]), int(waste_masc[1]),
               int(waste_masc[2]), int(waste_masc[3])]
    # bucle para calcular el prefix
    npart = 0
    prefix = 0
    while npart <= 3:
        bmaspart = bin(intmasc[npart])
        z = 2
        befast = False
        while z <= int(len(bmaspart)) and not befast:
            if str(bmaspart[-1]) == "1":
                prefix = prefix + 8
                befast = True
            elif str(bmaspart[z]) == "1":
                prefix = prefix + 1
            else:
                befast = True
            z = z + 1
        npart = npart + 1
    # calculo la cantidad de clientes posibles
    max_clients = (2**(32 - prefix))-2
    return {"myip": myip, "masc": masc, "ipx": ipx, "bro": bro, "gw": gw, "prefix": prefix, "max_clients": max_clients, "intipx": intipx}

def iptoHEX(ip):
    ipItems = ip.split(".")
    ipH = f"0x{int(ipItems[0]):02x}{int(ipItems[1]):02x}{int(ipItems[2]):02x}{int(ipItems[3]):02x}"
    return int(ipH, base=16)

def HEXtoip(hexip):
    real_hex = f"{str(hex(hexip))[2:10]:>08}"
    return f"{int(f'0x{real_hex[0:2]}', base=16)}.{int(f'0x{real_hex[2:4]}', base=16)}.{int(f'0x{real_hex[4:6]}', base=16)}.{int(f'0x{real_hex[6:8]}', base=16)}"

def scan(ip, vel):
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request = scapy.ARP(pdst=ip)
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=vel, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return (client_list)

def print_result(scan_total):
    print("IP\t\t\tMAC address\n--------------------------------------------------")
    i = 0
    scan_result = {}
    while i+1 <= len(scan_total):
        scan_result_list = scan_total[i]
        if scan_result_list != []:
            scan_result_dic = scan_result_list[0]
            print(scan_result_dic["ip"], "\t\t", scan_result_dic["mac"])
        i = i+1


# Variables, get info y enseñar-la x pantalla
i = 0
scan_total = []
on = True
# Menú principal
while on == True:
    eleccion = menu(0)
    if eleccion == 0:
        interface = input("interface? ")
        myinfo = get_info(interface)
        print("[+] INFO-OK")
        print(f'Mi IPv4: {myinfo["myip"]}\nIPv4 masc: {myinfo["masc"]}\nIPv4 de Red: {myinfo["ipx"]}\nIPv4 de broadcast: {myinfo["bro"]}\nIPv4 GateWay: {myinfo["gw"]}\nIPv4 prefix: {myinfo["prefix"]}\nIPv4 max clients: {myinfo["max_clients"]}')
    elif eleccion == 1:
        scaning = True
        while scaning == True:
            # Escojer el tipo de escaneo
            eleccion = menu(3)
            if eleccion == 0:
                interface = input("interface? ")
                myinfo = get_info(interface)
                barscan = ChargingBar('Escaneando:', max=myinfo["max_clients"])
                tragetcalc = (iptoHEX(myinfo["ipx"]))
                # Escojer el timeot de los paquetes ARP
                eleccion = menu(2)
                if 0 == eleccion:
                    vel = 0.005
                elif 1 == eleccion:
                    vel = 0.01
                elif 2 == eleccion:
                    vel = 0.05
                elif 3 == eleccion:
                    vel = 0.5
                elif 4 == eleccion:
                    vel = 1
                #Bucle de scans 1x1 (ip target)
                while i <= myinfo["max_clients"]:
                    barscan.next()
                    # Establecer el target o Objetivo
                    tragetcalc = tragetcalc + 1
                    target = HEXtoip(tragetcalc)
                    # Escaneo,guardar el resultado y impresion x pantalla
                    scan_result = scan(target, vel)
                    scan_total.append(scan_result)
                    subprocess.run("clear")
                    print_result(scan_total)
                    i = i + 1
                barscan.finish()
                print("[+]Red escaneada")
            elif eleccion == 1:
                # Bucle scans manuales
                target = ''
                while target != "ok":
                    target = input("target: ")
                    scan_result = scan(target, 1)
                    scan_total.append(scan_result)
                    subprocess.run("clear")
                    print_result(scan_total)
                    print("[+]Escaneo enviado")
            scaning = False
    elif eleccion == 2:
        on = False
