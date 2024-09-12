library(data.table)

#directorio <- "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/Dataset RAW/"
directorio <- "/Users/ionikullock/Desktop/TD VI/Trabajo práctico 2/Datos"

# 2. Obtener una lista de todos los archivos CSV en el directorio
archivos <- list.files(path = directorio, pattern = "\\.csv$", full.names = TRUE)

#directorio1 <- "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/clicked/"
#directorio0 <- "C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/not/"
directorio1 <- "/Users/ionikullock/Desktop/TD VI/Trabajo práctico 2/Datos/clicked"
directorio0 <- "/Users/ionikullock/Desktop/TD VI/Trabajo práctico 2/Datos/not"

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
  fwrite(df_filtrado1, file.path(directorio1, clicked))
  fwrite(df_filtrado0, file.path(directorio0, not))
}


unir_csvs <- function(directorio, archivo_salida) {
  # Obtener la lista de archivos CSV en el directorio
  archivos_csv <- list.files(path = directorio, pattern = "*.csv", full.names = TRUE)
  
  # Leer y combinar los archivos CSV en un solo data frame
  data_unida <- do.call(rbind, lapply(archivos_csv, read.csv))
  
  # Guardar el data frame combinado en un nuevo archivo CSV
  write.csv(data_unida, archivo_salida, row.names = FALSE)
  
  cat("Archivos combinados exitosamente en", archivo_salida, "\n")
}

# Ejemplo de uso
directorio <- "/Users/ionikullock/Desktop/TD VI/Trabajo práctico 2/Datos/not"
archivo_salida <- "not.csv"
unir_csvs(directorio, archivo_salida)