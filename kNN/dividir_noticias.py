import herramientas as ha

#Rutas de los archivos a usar y el porcentaje de noticias que se usarán para entrenar el modelo
ruta_noticias = 'archivos/noticias.csv'
ruta_palabras_clave = 'archivos/palabras_clave.csv'
ruta_categorias = 'archivos/categorias.csv'
ruta_noticias_entrenamiento = 'archivos/noticias_entrenamiento.csv'
ruta_noticias_test = 'archivos/noticias_test.csv'
ruta_categorias_entrenamiento = 'archivos/categorias_entrenamiento.csv'
ruta_categorias_test = 'archivos/categorias_test.csv'


def divide(ratio_noticias_entrenamiento):
    if ratio_noticias_entrenamiento < 0.01:
        ratio_noticias_entrenamiento = 0.01
    
    #Cargar las noticias, sus categorías y las palabras clave
    noticias = ha.leer_multiples_noticias(ruta_noticias)
    categorias = ha.leer_categorias(ruta_categorias)

    #Dividir las noticias en conjuntos y guardarlos en archivos separados
    noticias_categorizadas = ha.categorizar_noticias(noticias, categorias)
    noticias_entrenamiento, noticias_test = ha.dividir_noticias(noticias_categorizadas, ratio_noticias_entrenamiento)
    res1  = ha.guardar_noticias_entrenamiento_test(noticias_entrenamiento,noticias_test,ruta_noticias_entrenamiento,ruta_categorias_entrenamiento,ruta_noticias_test,ruta_categorias_test)
    res2 = 'El ratio de noticias de entrenamiento es: '+str(ratio_noticias_entrenamiento)
    print(res1+'\n'+res2)
    return res1+'\n'+res2

