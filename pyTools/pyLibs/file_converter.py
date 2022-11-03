import pandas as pd

def excel_2_csv(path:str,verbose=True):
    """Converteix el fitxer xlsx, xls o odf de la ruta entrada en csv

    Args:
        path (str): Ruta de l'arxiu
        verbose (bool, optional): Escolleix si ha de printar el proces. Defaults to True.

    Returns:
        str: La ruta del nou arxiu
    """
    if path[-4:].lower() == ".xls":
        read_file = pd.read_excel(path,engine="xlrd")
        new_path = path[0:-4]+".csv"
    elif path[-5:].lower() == ".xlsx":
        read_file = pd.read_excel(path)
        new_path = path[0:-5]+".csv"
    elif path[-4:].lower() == ".odf" or path[-4:] == ".odt" or path[-4:] == ".ods":
        read_file = pd.read_excel(path,engine="odf")
        new_path = path[0:-5]+".csv"
        
    read_file.to_csv (new_path, index = None, sep=";")
    
    if verbose:
        print ("[+] Document EXCEL convertit a CSV")
    
    return new_path

def csv_2_xlsx(path:str,verbose=True):
    """Converteix el fitxer csv de la ruta entrada en xlsx

    Args:
        path (str): Ruta de l'arxiu
        verbose (bool, optional): Escolleix si ha de printar el proces. Defaults to True.

    Returns:
        str: La ruta del nou arxiu
    """
    df = pd.read_csv(path)
    new_path = path[0:-4]+".xlsx"
    df.to_excel(new_path, sheet_name="fulla 1", index=False)
    if verbose:
        print ("[+] Document CSV convertit a XLSX")
    return new_path