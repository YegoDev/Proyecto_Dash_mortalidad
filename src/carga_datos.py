import pandas as pd 
import time
import os 

def cargar_datos(): 
    '''Carga las 3 entidades del modelo en data frames de pandas: mortalidad, causas de muerte y locacaciones'''

    inico = time.time()

    ruta = "data/anexo1.csv"
    print("Verificando si existe el archivo:", ruta)
    print("Ruta absoluta:", os.path.abspath(ruta))
    print("¿Existe?:", os.path.exists(ruta))
    
    df_mortalidad = pd.read_csv("data/anexo1.csv")       # Cargo la fuente de hechos  
   
    df_causas_muerte = pd.read_csv("data/Anexo2.CodigosDeMuerte_CE_15-03-23.csv")        # Cargo la fuente de la dimensión de causas 

    df_causas_muerte.columns = [        #Cambio los nombres de las colummas  de df_causas_muerte                                                           
        'CAPITULO',
        'NOMBRE_CAPITULO',
        'CODIGO_CIE10_3C',
        'DESCRIPCION_CIE_3C',
        'CODIGO_CIE10_4C',
        'DESCRIPCION_CIE_4C'
    ]

    df_locaciones = pd.read_csv("data/Anexo3.Divipola_CE_15-03-23.csv")      # Cargo la fuente de la dimensión de localidades

    return df_mortalidad, df_causas_muerte, df_locaciones

def transformar_datos(df_mortalidad, df_causas_muerte, df_locaciones): 
    """Realiza las transformaciones necesarias de los data frame, para consolidar la información"""

    # Aseguro que los codigos sean cadenas sin espacios 
    df_mortalidad["COD_MUERTE"] = df_mortalidad["COD_MUERTE"].astype(str)
    #df_mortalidad["COD_DEPARTAMENTO"] = df_mortalidad["COD_DEPARTAMENTO"].astype(str)
    df_mortalidad["COD_MUNICIPIO"] = df_mortalidad["COD_MUNICIPIO"].astype(str)
    df_causas_muerte["CODIGO_CIE10_4C"] = df_causas_muerte["CODIGO_CIE10_4C"].astype(str)
    #df_locaciones["COD_DEPARTAMENTO"] = df_locaciones["COD_DEPARTAMENTO"].astype(str).str.zfill(2).str.strip()
    df_locaciones["COD_MUNICIPIO"] = df_locaciones["COD_MUNICIPIO"].astype(str)

    #Agrego una X a todos los codigos de muerte que tienen solo 3 caracteres
    df_mortalidad["COD_MUERTE"] = df_mortalidad["COD_MUERTE"].astype(str)
    df_mortalidad["COD_MUERTE"] = df_mortalidad["COD_MUERTE"].apply(
        lambda x: x if len(x) == 4 else x + "X"
    )
    
    #Realizo el primer merge entre mortalidad y causas de muerte
    df_mortalidad_cons = df_mortalidad.merge(df_causas_muerte, left_on="COD_MUERTE", right_on="CODIGO_CIE10_4C", how="left")

    #Realizo el segundo merge entre mortalidad resultante y locaciones 
    df_mortalidad_cons = df_mortalidad_cons.merge(
        df_locaciones[["COD_DEPARTAMENTO", "COD_MUNICIPIO", "DEPARTAMENTO", "MUNICIPIO"]],
        on=["COD_DEPARTAMENTO", "COD_MUNICIPIO"],
        how="left"
    )

    return df_mortalidad_cons


if __name__ == "__main__": 
    df_hechos, df_causa, df_loc = cargar_datos()
    df = transformar_datos(df_hechos, df_causa, df_loc)
    print(df.columns)
    print(df.shape)
    print(df.head())
