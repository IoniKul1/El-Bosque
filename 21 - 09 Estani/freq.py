import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import OneHotEncoder

# Function to calculate category proportions based on the "Label" column
def calculate_category_ratios(df, cat_column):
    # Get counts of each category for label = 1 and label = 0
    label_counts = df.groupby([cat_column, 'Label']).size().unstack(fill_value=0)
    
    # Consider only the top 20 categories for each label
    top_categories_1 = label_counts[1].nlargest(20).index
    top_categories_0 = label_counts[0].nlargest(20).index
    
    top_categories = top_categories_1.intersection(top_categories_0)
    
    # Filter to keep only top 20 categories
    label_counts = label_counts.loc[top_categories]
    
    # Calculate proportions for label = 1 and label = 0
    total_1 = label_counts[1].sum()
    total_0 = label_counts[0].sum()
    
    prop_1 = (label_counts[1] / total_1)
    prop_0 = (label_counts[0] / total_0)

    if total_1 == 0:
        if prop_0 > 0.01:
            prop_1 = prop_0 / 2
        else:
            prop_1 = prop_0

    if total_0 == 0:
        if prop_1 > 0.01:
            prop_0 = prop_1 / 2
        else:
            prop_0 = prop_1

    # Calculate the ratio between proportions
    label_counts['ratio'] =  prop_1 / prop_0
    
    # Identify categories that need one-hot encoding
    label_counts['one_hot'] = np.where((label_counts['ratio'] < 0.95) | (label_counts['ratio'] > 1.05), True, False)
    
    return label_counts

# Function to apply one-hot encoding based on calculated category ratios
def apply_one_hot_encoding(df, columnas_excluidas, val, test):
    i = 1
    for col in df.columns:
        if col not in columnas_excluidas and col != 'Label': 

            category_info = calculate_category_ratios(df, col)
        
            # Select categories for one-hot encoding and "other"
            one_hot_categories = category_info[category_info['one_hot']].index.tolist()
            
            other = 'other_' + col

            # Replace categories not in one_hot_categories with "other"
            one_hot_categories = category_info[category_info['one_hot']].index.tolist()
            other = 'other_' + col

            # Replace categories not in one_hot_categories with "other"
            df[col] = df[col].apply(lambda x: x if x in one_hot_categories else other)
            val[col] = val[col].apply(lambda x: x if x in one_hot_categories else other)
            test[col] = test[col].apply(lambda x: x if x in one_hot_categories else other)
            
            print(i)
            i += 1
    
    
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output = True)
    categorical_columns = [col for col in df.columns if col not in columnas_excluidas and col != 'Label']
    print("fit")
    encoder.fit(df[categorical_columns])

    # Codificar los datos de entrenamiento, validación y prueba
    print("train")
    encoded_train = pd.DataFrame.sparse.from_spmatrix(encoder.transform(df[categorical_columns]), columns=encoder.get_feature_names_out())
    print("val")
    encoded_val = pd.DataFrame.sparse.from_spmatrix(encoder.transform(val[categorical_columns]), columns=encoder.get_feature_names_out())
    print("test")
    encoded_test = pd.DataFrame.sparse.from_spmatrix(encoder.transform(test[categorical_columns]), columns=encoder.get_feature_names_out())

    # Combinar las columnas codificadas con las columnas que no fueron codificadas
    print("train")
    encoded_train = pd.concat([df.drop(columns=categorical_columns), encoded_train], axis=1)
    print("val")
    encoded_val = pd.concat([val.drop(columns=categorical_columns), encoded_val], axis=1)
    print("test")
    encoded_test = pd.concat([test.drop(columns=categorical_columns), encoded_test], axis=1)
    
    print(f"Original number of rows: {df.shape[0]}")
    print(f"Number of rows after encoding: {encoded_train.shape[0]}")

    return encoded_train, encoded_val, encoded_test
    
print("leo val")
val = pd.read_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Val.csv") 
# El dataset sin as columnas que elegimos, no es necesario para filtrar el test. Podes modificar la funcion apply_one_hot_encoding, para que no use val y te va a modificar el test.
print("leo test")
test= pd.read_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Data TEST/one-hot/test filtrado.csv") # Le saca las columnas que elegimos

print("Por leer train...")
archivo = "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/Basicos/Train.csv" # El dataset sin as columnas que elegimos
df = pd.read_csv(archivo)
print("Leido!")
columnas_excluidas = ["Label",'auction_bidfloor', 'auction_time', "creative_height", "creative_width", "has_video"]  # Reemplaza con los nombres de las columnas que NO quieres modificar
print("por encodear")
df_encoded, val, test = apply_one_hot_encoding(df, columnas_excluidas, val, test)
print("listooooooo")

print("a guardar el traino")
# Guardar el dataset actualizado
df_encoded.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/one-hot/freq.csv", index=False)

print("a guardar el val")
val.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/one-hot/val.csv", index=False)

print("a guardar el test")
test.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Data TEST/one-hot/test filtrado oh.csv", index=False)

print("Valores actualizados y guardados")