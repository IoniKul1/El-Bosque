import pandas as pd
import numpy as np
import json

# Cargar el dataset
print("Por leer...")
archivo = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Train.csv"
datos = pd.read_csv(archivo)
print("Leido!")

# Separar el dataset en dos partes basadas en 'Label'
datos_0 = datos[datos['Label'] == 0]
datos_1 = datos[datos['Label'] == 1]

# Lista de columnas en las que no quieres realizar la transformación
columnas_excluidas = ['auction_bidfloor', 'auction_time', "creative_height", "creative_width"]  # Reemplaza con los nombres de las columnas que NO quieres modificar

# Diccionario para almacenar los diccionarios de valores para cada columna
diccionarios_valores = {} 

# Procesar solo las columnas que no están en la lista de columnas excluidas
for columna in datos.columns:
    if columna not in columnas_excluidas and columna != 'Label':  # Excluir columnas en la lista y 'Label'
        # Calcular la frecuencia de cada valor en ambos datasets
        freq_0 = datos_0[columna].value_counts()
        freq_1 = datos_1[columna].value_counts()

        # Calcular las proporciones
        proporcion_0 = freq_0 / len(datos_0)
        proporcion_1 = freq_1 / len(datos_1)

        # Calcular la razón de proporciones y aplicar logaritmo
        valores_nuevos = {}
        for valor in proporcion_1.index:
            p1 = proporcion_1.get(valor, 0)
            p0 = proporcion_0.get(valor, 0)
            if p0 > 0:
                razon = p1 / p0
                valores_nuevos[valor] = round(np.log(razon), 4)
            else:
                valores_nuevos[valor] = np.nan  # Si p0 es 0, asignar NaN

        # Actualizar los valores en el dataset original
        datos[columna] = datos[columna].map(valores_nuevos)

        datos[columna] = datos[columna].fillna(0)

        # Guardar el diccionario de valores para la columna
        diccionarios_valores[columna] = valores_nuevos

    if columna in columnas_excluidas and columna != 'Label':
        med_0 = datos_0[columna].median(skipna=True)
        med_1 = datos_1[columna].median(skipna=True)

        print(columna)
        medmed = (med_0 + med_1)/2
        print(medmed)
        datos[columna] = datos[columna].fillna(medmed)


print("procesado")
# Guardar el diccionario de valores para todas las columnas
with open("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Div Prop/diccionarios_valores.json", 'w') as f:
    json.dump(diccionarios_valores, f)

print("Listo el diccionario")
# Guardar el dataset actualizado
datos.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Div Prop/log.csv", index=False)

print("Valores actualizados y guardados en: log.csv")
print("Diccionario de valores para cada columna guardado en: diccionarios_valores.json")
