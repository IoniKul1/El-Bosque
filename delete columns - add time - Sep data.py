import os
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split

# Definir la carpeta de origen y destino
carpeta_origen = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Dataset RAW"
carpeta_destino = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Dataset FILTER"

# Definir las columnas a eliminar
columnas_a_borrar = ["device_id", "creative_categorical_10","auction_boolean_1", "auction_boolean_2", "auction_categorical_2", "auction_categorical_3",
                        "auction_categorical_10", "auction_categorical_8", "auction_categorical_9", "auction_categorical_7", "action_categorical_2", "auction_age", "timezone_offset",
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



# Definir la carpeta de origen y el nombre del archivo combinado
carpeta_origen = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Dataset FILTER"
archivo_destino = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Dataset FILTER/union filter.csv"

# Obtener la lista de archivos CSV en la carpeta de origen
archivos_csv = [f for f in os.listdir(carpeta_origen) if f.endswith('.csv')]

# Crear una lista para almacenar los DataFrames
dataframes = []

# Iterar sobre cada archivo CSV y agregarlo a la lista
for archivo in archivos_csv:
    ruta_archivo = os.path.join(carpeta_origen, archivo)
    datos = pd.read_csv(ruta_archivo)
    dataframes.append(datos)
    os.remove(ruta_archivo)

# Combinar todos los DataFrames en uno solo
union_df = pd.concat(dataframes, ignore_index=True)

# Guardar el DataFrame combinado en un archivo CSV
union_df.to_csv(archivo_destino, index=False)

print(f"Archivos combinados en: {archivo_destino}")

archivo = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Dataset FILTER/union filter.csv"
datos = pd.read_csv(archivo)
print("leido el filter")

print("reduccion")
# Split 90% for test, 10% for further splits
datos_red, _ = train_test_split(datos, test_size=0.90, random_state=42)

print("separo")
# Split 85% of remaining data into train and 15% into temp
train_red, temp = train_test_split(datos_red, test_size=0.15, random_state=42)
print(f"Train size: {len(train_red)}, Temp size: {len(temp)}")

# Make sure there are enough samples in temp before splitting
if len(temp) > 1:
    print("separo otra vez")
    # Split temp into val (50%) and test (50%)
    val_red, test_red = train_test_split(temp, test_size=0.50, random_state=42)
    print(f"Val size: {len(val_red)}, Test size: {len(test_red)}")
else:
    print("Not enough samples in temp for further splitting.")

# Guardar los conjuntos en archivos CSV en una ubicación específica
train_red.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Train_red.csv", index=False)
val_red.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Val_red.csv", index=False)
test_red.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Test_red.csv", index=False)

print("Conjuntos reducidos creados y guardados")


print("separo")
# Split 85% of remaining data into train and 15% into temp
train, temp = train_test_split(datos, test_size=0.15, random_state=42)
val, test = train_test_split(temp, test_size=0.50, random_state=42)
print(f"Val size: {len(val)}, Test size: {len(test)}")


train.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Train.csv", index=False)
val.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Val.csv", index=False)
test.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Test.csv", index=False)

print("Conjuntos creados y guardados: Train.csv, Val.csv, Test.csv")