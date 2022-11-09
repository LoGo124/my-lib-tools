import subprocess

#from simple_term_menu import TerminalMenu as tmenu

from pyLibs.Net_tools import netCalc as nc
import pyLibs.Config_tools as ct


class main:
    def __init__(self):
        m1={"1":"Crear configuración",
            "2":"Modificar configuración",
            "3":"Salir"}
        m2={"1":"Modificar",
            "2":"Guardar",
            "3":"Aplicar",
            "4":"<---'"}

        while (True):
            opt = self.printMenu(m1)

            if (opt == 1):
                self.conf = ct.config(**self.new_conf())#dict_config={"program_path":"C:/Users/IGNUser/Documents/GitHub/my-lib-tools/pyTools","ipx":config.ipx,"masc":config.masc,"ranges":config.ranges,"ipr":config.ipr,"dns":config.dns,"dlt":config.dlt,"mlt":config.mlt}
                print(self.conf2str())
                input("wait")
                self.conf.safe_config("C:/Users/IGNUser/Documents/GitHub/my-lib-tools/configsDhcp/dhcp1.json")
            elif(opt == 2):
                ruta = input("Ruta del fichero json de configuración: ")
                self.importConf(ruta)
                print(self.conf2str())
                opt2 = self.printMenu(m2)
                if (opt2 == 1):
                    m3 = {"1":"Ip de red: "+str(self.ipx),
                          "2":"Mascara de red: "+str(self.masc),
                          "3":"Rangos de ip's: "+str(self.ranges),
                          "4":"Ip de router: "+str(self.ipr),
                          "5":"Servidores de nombres: "+str(self.dns),
                          "6":"Default lease time: "+str(self.dlt),
                          "7":"Max lease time: "+str(self.mlt),
                          "8":"<---'"}
                    opt3 = self.printMenu(m3)
                elif (opt2 == 2):
                    self.conf.safe_config(ruta)
                elif (opt2 == 3):
                    pass
                elif (opt2 == 4):
                    pass
            elif(opt == 3):
                print("Espero haber sido de ayuda ADIOS!")
                break

    def new_conf(self,dict_config={"ipx":[192,168,1,0], "masc":[255,255,255,0], "ranges":[[[192,168,1,50],[192,168,1,200]]], "ipr":[192,168,1,1], "dns":[[8,8,8,8], [8,8,4,4]], "dlt":600, "mlt":7200}):
        for param in dict_config:
            try:
                exec("self."+param+" = "+str(dict_config[param]))
            except SyntaxError:
                exec("self."+param+" = \""+str(dict_config[param])+"\"")
        self.dict_config=dict_config
        return self.dict_config
    
    def importConf(self,ruta):
        conf = ct.config(ruta)
        execStr = "self.new_conf(dict_config={"
        x = 0
        for param in conf:
            x += 1
            try:
                error = 42
                exec("error = "+str(param[1]))
                execStr += "\""+param[0]+"\":"+str(param[1])
                del error
            except SyntaxError:
                execStr += "\""+param[0]+"\":\""+str(param[1])+"\""
            if not(x == len(conf)):
                execStr += ","
        execStr +=  "})"
        exec(execStr)

            
    
    #self.ipx = nc.ask_ip(mensaje="Ip de red: ")
    #self.masc = nc.ask_masc()
    #self.ranges = []
    #for item in range(0,int(input("Cuantos rangos quieres hacer? "))):
    #    self.ranges.append([nc.ask_ip("Ip inicio: "), nc.ask_ip("Ip fin: ")])
    #self.ipr = nc.ask_ip(mensaje="Ip del router: ")
    #self.dns = []
    #for item in range(0,int(input("Cuantos dns quieres poner? "))):
    #    self.dns.append(nc.ask_ip("DNS "+str(item+1)+": "))

    def conf2str(self):
        confStr = "default-lease-time "+str(self.dlt)+";\n"
        confStr += "max-lease-time "+str(self.mlt)+";\n\n"
        confStr += "subnet "+str(self.ipx[0])+"."+str(self.ipx[1])+"."+str(self.ipx[2])+"."+str(self.ipx[3])+" netmask "+str(self.masc[0])+"."+str(self.masc[1])+"."+str(self.masc[2])+"."+str(self.masc[3])+"{\n"
        for range in self.ranges:
            confStr += "\trange "+str(range[0][0])+"."+str(range[0][1])+"."+str(range[0][2])+"."+str(range[0][3])+" "+str(range[1][0])+"."+str(range[1][1])+"."+str(range[1][2])+"."+str(range[1][3])+";\n"
        confStr += "\toption routers "+str(self.ipr[0])+"."+str(self.ipr[1])+"."+str(self.ipr[2])+"."+str(self.ipr[3])+";\n"
        confStr += "\toption domain-name-servers"
        for dns in self.dns:
            confStr += " "+str(dns[0])+"."+str(dns[1])+"."+str(dns[2])+"."+str(dns[3])+""
            if not(dns == self.dns[len(self.dns)-1]):
                confStr += ","
            else:
                confStr += ";\n"
        confStr += "}\n"
        return confStr

    def saveConf(path="/etc/dhcp/dhcpd.conf"):
        with open(path,"w") as file:
            pass
    
    def printMenu(self, opciones):
        print(" "+"_"*70+" _ ")
        print("/"+"_"*70+"/ |")
        print("/"+"\\/"*35+"| |")
        print("|"+" "*70+"| |")
        for n in opciones:
            print(f"|{n:>4} = {opciones[n]:63}| |")
        print("|"+" "*70+"| |")
        print("\\"+"_"*70+"/_/")
        r = input(">> ")
        if r in opciones:
            return int(r)
        else:
            return self.printMenu(opciones)

main()

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