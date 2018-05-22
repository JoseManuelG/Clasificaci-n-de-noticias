import herramientas as ha
import knn

#rutas por defecto de los archivos para entrenamiento
ruta_noticias_entrenamiento = 'archivos/noticias_entrenamiento.csv'
ruta_palabras_clave = 'archivos/palabras_clave.csv'
ruta_archivo_entrenamiento = 'archivos/entrenamiento.csv'
ruta_archivo_f_doc = 'archivos/frecuencias_documentales_inversas.csv'


def entrenar():
    # cargar las noticias de entrenamiento y todas las palabras clave para entrenar el modelo
    noticias = ha.leer_noticias_entrenamiento(ruta_noticias_entrenamiento)
    palabras_clave = ha.leer_palabras_clave(ruta_palabras_clave)

    #Entrenar el modelo
    matriz_frecuencias = knn.frecuencia_de_terminos_en_documentos(noticias,palabras_clave)
    f_documentales = knn.frecuencias_documentales(noticias,palabras_clave)
    f_documentales_inv = knn.frecuencias_documentales_inversas(len(palabras_clave),len(noticias),f_documentales)
    pesos = knn.pesos_de_terminos_en_documentos(matriz_frecuencias,f_documentales_inv)

    #Guardar los datos producidos por el entrenamiento
    ha.guardar_frecuencias_documentales_inversas(f_documentales_inv,ruta_archivo_f_doc)
    ha.guardar_pesos(pesos,ruta_archivo_entrenamiento)
    res = str(len(pesos[0]))
    print('Modelo entrenado con',res,"noticias de entrenamiento.")
    return res
