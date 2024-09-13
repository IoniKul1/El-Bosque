import os
import pandas as pd
from datetime import datetime

# Definir la carpeta de origen y destino
carpeta_origen = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Dataset RAW"
carpeta_destino = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Dataset FILTER"

# Definir las columnas a eliminar
columnas_a_borrar = ["device_id", "creative_categorical_10","auction_boolean_1", "auction_boolean_2" "auction_categorical_6",
                      "auction_categorical_7", "auction_categorical_8", "auction_categorical_10", "auction_age", "timezone_offset",
                        "action_list_1","action_list_2", "auction_list_0"]  # A "action_list_1", "action_list_2" y "auction_list_0"
                                                                 # los eliminamos hasta que los hayamos analizado correctamente

# Función para extraer la hora desde epoch
def extraer_hora(epoch_time):
    return datetime.utcfromtimestamp(epoch_time).hour

# Obtener la lista de archivos CSV en la carpeta de origen
archivos_csv = [f for f in os.listdir(carpeta_origen) if f.endswith('.csv')]

# Iterar sobre cada archivo CSV
for archivo in archivos_csv:
    # Leer el archivo CSV
    ruta_archivo = os.path.join(carpeta_origen, archivo)
    datos = pd.read_csv(ruta_archivo)
    
    # Eliminar las columnas deseadas
    datos_modificado = datos.drop(columns=columnas_a_borrar, errors='ignore')
    
    # Si existe la columna "auction_time", convertirla a la hora
    if 'auction_time' in datos_modificado.columns:
        datos_modificado['auction_time'] = datos_modificado['auction_time'].apply(extraer_hora)
    
    # Generar el nombre del archivo en la carpeta de destino
    ruta_destino = os.path.join(carpeta_destino, archivo)
    
    # Guardar el archivo modificado en la carpeta de destino
    datos_modificado.to_csv(ruta_destino, index=False)


print("Listo!")