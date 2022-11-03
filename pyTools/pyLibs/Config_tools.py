from json import dump, load
from tkinter import filedialog, messagebox

from datetime import datetime
from getpass import getuser

class config:
    def __init__(self,json_path):
        try:
            with open(json_path,"r",encoding="UTF-8") as json_file:
                dict_config = load(json_file)
        except:
            messagebox.showerror("Config not found","No se ha encontrado el fitxero de configuración.")
            with filedialog.askopenfile("r",defaultextension="json") as json_file:
                dict_config = load(json_file)
        self.user_path = "C:/Users/"+getuser()
        #   MODO MANUAL
        #Añade todos los parametros k se deberian encontrar en el json
        self.program_path = dict_config["program_path"]
        #Añade los nombres de las variables
        self.param = ["program_path"]
        #   MODO AUTO
        ##for param in dict_config:
        ##    exec("self."+param+" = "+dict_config[param])
            
    def __iter__(self):
        """Converteix la clase en un iterable i inicialitza el contador

        Returns:
            obj: es retorna a si mateix
        """
        self.i = 0
        return self

    def __next__(self):
        """Contribueix al funcionament de la funció __iter__ retornant els valors que volem, que en aquest cas son els parametres de configuracio del programa.

        Raises:
            StopIteration: Executa aquest error per deixar de iterar l'objecte i d'aquesta manera indicar que no hi han mes parametres

        Returns:
            list: lista amb el nom de la variable i el seu valor.
        """
        if self.i < len(self.param):
            key = self.param[self.i]
            value = eval("self."+self.param[self.i])
        else:
            raise StopIteration
        self.i += 1
        return [key,value]

    def safe_config(self,json_path):
        """Guarda les dades de totes les variables especificades en la llista param definida a __init__() en un fitxer json en la ruta donada.

        Args:
            json_path (str): ruta + nom + extensio d'on es guardaran les dades
        """
        dict_config = {}
        for param in self:
            dict_config[param[0]] = param[1]
        with open(json_path,"w") as json_file:
            dump(dict_config,json_file)

    def restaurar_backup(self):
        """Demana amb el dialog del sistema quin fitxer de configuració volem restaurar pero no substitueix el predefinit
        """
        with open(filedialog.askopenfilename(defaultextension=".json",initialdir= self.program_path + "/backups"),"r",encoding="UTF-8") as json_file:
            dict_config = load(json_file)
            
        for parametro in self.param:
            exec("self." + parametro + " = dict_config[\"" + parametro + "\"]")

    def auto_backup(self):
        """Crea una copia de seguretat de utilitzant la funcio de safe_config() i li dona una ruta generada amb 
        el valor de la ruta del mateix programa, en una subcarpeta de backups amb un nom auto generat en base a la data i hora.
        """
        now = datetime.now()
        ruta = self.program_path+"/backups/"+now.strftime("%d-%m-%y %H-%M-%S")+" info.json"
        self.safe_config(ruta)

    def reemplaza_param(self,key,value):
        """Utilitza la funció exec per canviar/crear el valor de cualsevol variable de l'objecte, NO O GUARDA.

        Args:
            key (str): Nom del parametre que es vol configurar
            value (str): Valor del parametre, ha de estar en string independentment de el format del valor(funcio exec()))
        """
        exec("self." + key + " = value")
