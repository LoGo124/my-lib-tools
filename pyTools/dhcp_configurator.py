from pyLibs.Net_tools import netCalc

nc = netCalc
class dhcp_conf:
    def __init__(self, dlt = 600, mlt = 7200):
        self.ipx = nc.ask_ip(mensaje="Ip de red: ")
        self.masc = nc.ask_masc()
        self.ranges = []
        for item in range(0,int(input("Cuantos rangos quieres hacer? "))):
            self.ranges.append([nc.ask_ip("Ip inicio: "), nc.ask_ip("Ip fin: ")])
        self.ipr = nc.ask_ip(mensaje="Ip del router: ")
        self.dns = []
        for item in range(0,int(input("Cuantos dns quieres poner? "))):
            self.dns.append(nc.ask_ip("DNS "+str(item+1)+": "))
        self.dlt = dlt
        self.mlt = mlt

    def print_config(self):
        print("\n--- ESTO ES UNA MUESTRA DEL ARXIVO QUE SE GENERARA ---")
        print("")
        print(f"default-lease-time {self.dlt};")
        print(f"max-lease-time {self.mlt};\n")
        print(f"subnet {self.ipx[0]}.{self.ipx[1]}.{self.ipx[2]}.{self.ipx[3]} netmask {self.masc[0]}.{self.masc[1]}.{self.masc[2]}.{self.masc[3]}",end="")
        print("{")
        for range in self.ranges:
            print(f"\trange {range[0][0]}.{range[0][1]}.{range[0][2]}.{range[0][3]} {range[1][0]}.{range[1][1]}.{range[1][2]}.{range[1][3]};")
        print(f"\toption routers {self.ipr[0]}.{self.ipr[1]}.{self.ipr[2]}.{self.ipr[3]}")
        print("\toption domain-name-servers",end="")
        for dns in self.dns:
            print(f" {dns[0]}.{dns[1]}.{dns[2]}.{dns[3]}",end="")
            if not(dns == self.dns[len(self.dns)-1]):
                print(",",end="")
            else:
                print(";")
        print("}\n")
    

def Menu(opciones):
    print("|"+"-"*41+"|")
    print("|"+" "*41+"|")
    for n in opciones:
        print(f"|{n:>4} = {opciones[n]:34}|")
    print("|"+" "*41+"|")
    print("|"+"-"*41+"|")
    r = input(">> ")
    if r in opciones:
        return int(r)
    else:
        return Menu(opciones)
    
opciones = {"1":"Crear fixero",
            "2":"Modificar fixero",
            "3":"Salir"}

while (True):
    opt = Menu(opciones)

    if (opt == 1):
        config = dhcp_conf()
        config.print_config()
    elif(opt == 2):
        print("Esta función esta en desarrollo")
    elif(opt == 3):
        print("Espero haber sido de ayuda ADIOS!")
        break
    
# minimal sample /etc/dhcp/dhcpd.conf
#default-lease-time 600;
#max-lease-time 7200;
#
#subnet 192.168.1.0 netmask 255.255.255.0 {
# range 192.168.1.50 192.168.1.250;
# option routers 192.168.1.254;
# option domain-name-servers 8.8.8.8, 8.8.4.4, 127.0.0.1;
# option domain-name "mydomain.example";
#}