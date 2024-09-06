library(data.table)

directorio <- "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/Dataset RAW/"

# 2. Obtener una lista de todos los archivos CSV en el directorio
archivos <- list.files(path = directorio, pattern = "\\.csv$", full.names = TRUE)

directorio1 <- "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/clicked/"
directorio0 <- "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/not/"

for (archivo in archivos) {
  
  # 4. Leer el archivo CSV
  df <- fread(archivo)
  
  # Filtrar las filas donde la columna 'Label' tiene valor 1
  df_filtrado1 <- df[Label == 1]
  df_filtrado0 <- df[Label == 0]
  
  # Crear el nombre del archivo nuevo (agregar _filtrado al nombre original)
  clicked <- paste0(tools::file_path_sans_ext(basename(archivo)), "_clicked.csv")
  not <- paste0(tools::file_path_sans_ext(basename(archivo)), "_not.csv")
  
  # Guardar el dataframe filtrado en la misma carpeta
  fwrite(df_filtrado, file.path(directorio1, clicked))
  fwrite(df_filtrado, file.path(directorio0, not))
}
