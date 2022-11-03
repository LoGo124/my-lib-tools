def print_menu(opciones):
    print("|"+"-"*40+"|")
    print("|"+" "*40+"|")
    for n in opciones:
        print(f"|{n:>4} = {opciones[n]:33}|")
    print("|"+" "*40+"|")
    print("|"+"-"*40+"|")
    
opciones = {"1":"Crear fixer de configuración",
            "2":"Modificar fixero de configuración",
            "3":"Salir"}
print_menu(opciones)