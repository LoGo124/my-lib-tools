import subprocess
import optparse
import re
import time
import random


auto_mac_time = 5
auto_mac_loop_time = 30

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface", help="Escojer la interface que quieres editar")
    parser.add_option("-m", "--mac", dest = "new_mac", help="Cambiar la mac por la especificada")
    parser.add_option("-M", "--mac10min",dest = "enable_10m",  help="Cambiar la mac cada 10 min.")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error ("[-] Por favor indica una Interfaz, usa --help para mas info")
    elif not options.new_mac and not options.enable_10m:
        parser.error ("[-] Por favor indica la mac que quieres usar --help para mas info")
    return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_output(interface):
    ifconfig_output = subprocess.check_output(["ifconfig", options.interface])
    current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_output))
    if current_mac:
        return current_mac.group(0)
    else:  
        print("[-] No se pudo leer la direccion mac")

options = get_arguments()
interface = options.interface

current_mac = get_output (options.interface)

if options.enable_10m:
    sec = 0
    while sec <= auto_mac_loop_time:
        sec1 = 0
        while sec1 <= auto_mac_time:
            time.sleep(1)
            sec1= sec1 + 1
            sec = sec + 1
        making_mac = True
        hexf = "00:"
        while making_mac:
            randn = random.randrange(start=0x00, stop=0xff)
            if hex(randn)[-2] == "x" :
                hex1 = "0" + hex(randn)[-1]
            else:
                hex1 = hex(randn)[-2] + hex(randn)[-1]
            hexf = hexf + hex1
            if len(hexf) != 17:
                hexf = hexf + ":"
            else:
                making_mac = False
        new_mac = hexf
        print("[+] Cambiando Direccion Mac para " + interface + " a " + new_mac)
        change_mac (options.interface, new_mac)
        print ("anterior MAC = ", current_mac)
        current_mac = get_output (options.interface)
        if current_mac == new_mac:
            print ("[+] MAC cambio correctamente a " + str(current_mac))
        else:
            print ("[-] Mac no fue cambiada")        
else:
    new_mac = options.new_mac
    print("[+] Cambiando Direccion Mac para " + interface + " a " + new_mac)
    change_mac (options.interface, options.new_mac)
    print ("anterior MAC = ", current_mac)
    current_mac = get_output (options.interface)
    if current_mac == options.new_mac:
        print ("[+] MAC cambio correctamente a " + str(current_mac))
    else:
        print ("[-] Mac no fue cambiada")



