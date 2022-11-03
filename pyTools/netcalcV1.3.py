class netCalc:
    def __init__(self):
        aprobado = False
        while not aprobado:
            print ("]"+"\/"*25+"[\n]"+" "*50+"[\n]   1 = Numero de subxarxa ---> Prefix             [\n]   2 = Prefix ---> Numero de hosts + Mascara      [\n]   3 = Numero de hosts ---> Prefix                [\n]   4 = IP + Mascara ---> IP Xarxa & IP Broadcast  [\n]   5 = Ya he sacado un 10                         [\n]"+" "*50+"[\n]"+"\/"*25+"[")
            modo = input("Digues que vols calcular: ")
            if modo == "1":
                masc = self.ask_masc()
                prefix = self.masc2Prefix(masc)
                print (prefix)
            elif modo == "2":
                prefix = int(input("Prefix: "))
                resultat = self.Prefix2HostsIMasc(prefix)
                print(f"El teu num de Hosts es: {resultat[0]}")
                print ("La mascara es: ", resultat[1][0:-1])
            elif modo == "3":
                hosts = int(input("Hosts: "))
                resultat3 = self.hosts2Prefix(hosts)
                print (resultat3)
            elif modo == "4":
                ip = self.ask_ip()
                masc = self.ask_masc()
                ipxarxa, ipbroad = self.IpMasc2IpxIpb(ip, masc)
                print(f"La ip de la xarxa es: {ipxarxa[0]}.{ipxarxa[1]}.{ipxarxa[2]}.{ipxarxa[3]}")
                print(f"La ip broadcast de la xarxa es: {ipbroad[0]}.{ipbroad[1]}.{ipbroad[2]}.{ipbroad[3]}")
            elif modo == "5":
                aprobado = True
                print ("Felizidades por el aprobado, Edu y LoGo son tan buenos programadores que seguro que has sacado un 10")
            else:
                print ("Introduce el numero correspondiente al modo que quieras usar(Un numero del 1 al 7).")
            input("-----Press enter to continue-----")
    
    def masc2Prefix(self, masc):
        prefix = 0
        npart = 0
        while npart <= 3:
            bmaspart = bin(masc[npart])
            z = 2
            befast = False
            while z <= int(len(bmaspart)) and not befast:
                if str(bmaspart[-1]) == "1":
                    prefix += 8
                    befast = True
                elif str(bmaspart[z]) == "1":
                    prefix += 1
                else:
                    befast = True
                z += 1   
            npart += 1
        return prefix
    
    def Prefix2HostsIMasc(self, Prefix:int):
        nHosts = (2**(32 - Prefix))-2
        l1 = ("255.", "128.", "192.", "224.", "240.", "248.", "252.", "254.")
        #Divido el prefijo entre 8 para saber cuantas secciones de la mascara son 255
        r1 = int(int(Prefix) / 8)
        #El residuo es equivalente a la cantidad de 1's que hay en la unica sección que no es ni 0, ni 255
        r2 = int(int(Prefix) % 8)
        #Genera la parte de la mascara que solo son 255's
        mascara = l1[0] * r1
        #Genera el resto de la mascara
        if r2 != 0:
            #Utilizo el residuo para extraer de la lista el numero correspondiente
            mascara = mascara + l1[r2]
            mascara = mascara + ("0." * (3 - r1))
        #Atajo para cuando el residuo es 0
        else:
            mascara = mascara + ("0." * (4 - r1))
        return [nHosts,Prefix]
    
    def hosts2Prefix(self, hosts:int):
        return (32 - (len(bin(hosts)) - 2))

    def IpMasc2IpxIpb(args, ip, masc):
        ipx = [0,0,0,0]
        bipx = ""
        ipb = [0,0,0,0]
        bipb = ""
        #bucle que calcula la ip de red por partes
        npart = 0
        while npart <= 3:
            #traducir la seccion a binario
            bmascpart = bin(masc[npart])
            bippart = bin(ip[npart])
            #Corrige el binario en caso de haver omitido los 0's de la izquierda
            if len(bippart) != 10:
                bippart = bippart[0:2] + ("0" * (10 - len(bippart))) + bippart[2:]
            z = 2
            #Atajo para cuando la sección de la mascara es 255
            if str(bmascpart[-1]) == "1":
                ipx[npart] = ip[npart]
            #Atajo para cuando la sección de la mascara es 0
            elif str(bmascpart[2]) == "0":
                ipx[npart] = 0
            else:
                #Bucle para hacer el and con el binario i guardarlo en la variable bipx
                while z <= int(len(bmascpart))-1:
                    bipx = bipx + str(int(bippart[z]) * int(bmascpart[z]))
                    z = z + 1
                bipx = "0b"+bipx
                ipx[npart] = int(ipx[npart] + int(bipx,2))
            npart = npart + 1
        npart = 0
        while npart <= 3:
            bmascpart = bin(masc[npart])
            bippart = bin(ip[npart])
            if len(bippart) != 10:
                bippart = bippart[0:2] + ("0" * (10 - len(bippart))) + bippart[2:]
            z = 2
            if str(bmascpart[-1]) == "1":
                ipb[npart] = ip[npart]
            elif str(bmascpart[2]) == "0":
                ipb[npart] = 255
            else:
                while z <= int(len(bmascpart))-1:
                    if bmascpart[z] == "1":
                        bipb = bipb + bippart[z]
                    else:
                        bipb = bipb + "1"
                    z = z + 1
                bipb = "0b"+bipb
                ipb[npart] = int(ipb[npart] + int(bipb,2))
            npart = npart + 1
        return [ipx, ipb]
    
    def ask_masc(self):
        masc = [0,0,0,0]
        mascpart = ""
        i = 0
        npart = 0
        mascarainput = input ("Quina es la masscara? ")
        #bucle para guardar la mascara en enteros dentro de una lista
        while i <= len(mascarainput):
            if i <= len(mascarainput)-1:
                num1 = mascarainput[i]
            if num1 != '.' and not (i == len(mascarainput)):
                mascpart = mascpart + num1
            else:
                masc[npart] = int(mascpart)
                npart = npart + 1
                mascpart = ""
            i = i + 1
        i = 0
        npart = 0
        return masc

    def ask_ip(self):
        ip = [0,0,0,0]
        ippart = ""
        i = 0
        npart = 0
        ipinput = input ("Quina es la ip? ")
        #bucle para guardar la ip en enteros dentro de una lista
        while i <= len(ipinput):
            if i <= len(ipinput)-1:
                num1 = ipinput[i]
            if num1 != '.' and not(i == len(ipinput)):
                ippart = ippart + num1
            else:
                ip[npart] = ip[npart] + int(ippart)
                npart = npart + 1
                ippart = ""
            i = i + 1
        npart = 0
        i = 0
        return ip

start = netCalc()