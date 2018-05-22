from collections import Counter
import herramientas as ha
import knn

#Variables necesarias para el testeo de múltiples noticias
ruta_noticias_test = 'archivos/noticias_test.csv'
ruta_categorias_test = 'archivos/categorias_test.csv'
ruta_categorias_entrenamiento = 'archivos/categorias_entrenamiento.csv'
ruta_archivo_entrenamiento = 'archivos/entrenamiento.csv'
ruta_archivo_f_doc = 'archivos/frecuencias_documentales_inversas.csv'

#Variables necesarias para el testeo de una noticia
ruta_categorias = 'archivos/categorias_entrenamiento.csv'
#ruta_noticia_test = 'archivos/test_cultura.csv'

#Variables compartidas por ambos métodos
ruta_palabras_clave = 'archivos/palabras_clave.csv'



def testear_multiples_noticias(k):

    #Cargar las palabras clave y los datos producidos en el entrenamiento del modelo
    palabras_clave = ha.leer_palabras_clave(ruta_palabras_clave)
    conjunto_entrenamiento = ha.cargar_entrenamiento(ruta_archivo_entrenamiento)

    #Asignar a cada vector de pesos de una noticia su categoría correspondiente
    ha.cargar_categorias(ruta_categorias_entrenamiento, conjunto_entrenamiento)

    #Cargar categorías de las noticias del conjunto de prueba
    categorias_reales = ha.leer_categorias(ruta_categorias_test)

    #Cargar las noticias del conjunto de prueba
    noticias_test = ha.leer_noticias_entrenamiento(ruta_noticias_test)

    if int(k)>len(conjunto_entrenamiento):
        print('El k es demasiado grande, no puede ser mayor que ',len(conjunto_entrenamiento))
        return -1

    #Contar el número de apariciones de cada palabra clave en cada noticia del conjunto de prueba
    apariciones_de_palabras_clave_de_cada_noticia = ha.palabras_clave_multiples_noticias(noticias_test,palabras_clave,categorias_reales)

    #Cargar las frecuencias documentales inversas
    f_docs_inv = ha.cargar_frecuencias_documentales_inversas(ruta_archivo_f_doc)

    #Calcular los pesos
    pesos = [[apariciones_de_palabras_clave_de_cada_noticia[j][i]*f_docs_inv[i] for i in range(len(f_docs_inv))] for j in range(len(noticias_test))]

    #Estimar categorías para cada noticia
    categorias_estimadas = []
    for peso in pesos:
        vecinos = knn.escoger_vecinos(conjunto_entrenamiento, peso, int(k))
        categoria_del_documento, = Counter(vecinos).most_common(1)
        categorias_estimadas.append(categoria_del_documento[0])

    categorias_estimadas[:] = ['Cultura' if int(x) == 0 else 'Sociedad' if int(x) == 1 else 'Deporte' if int(x) == 2 else
    'Tecnología' if int(x) == 3 else 'Economía' if int(x) == 4 else 'Ciencia' if int(x) == 5 else 'Ninguna' for x in categorias_estimadas]

    categorias_reales[:] = ["Cultura" if int(x) == 0 else "Sociedad" if int(x) == 1 else "Deporte" if int(x) == 2 else
    "Tecnología" if int(x) == 3 else "Economía" if int(x) == 4 else "Ciencia" if int(x) == 5 else "Ninguna" for x in categorias_reales]

    #Efectividad del algoritmo
    aciertos = 0

    for i in range(len(categorias_reales)):
        if categorias_reales[i] == categorias_estimadas[i]:
            aciertos +=1
    print('El número de documentos categorizados es: ', len(categorias_estimadas))
    print('El número de documentos categorizados correctamente es: ',aciertos)

    porcentaje = 0
    if len(categorias_estimadas) !=0:
        porcentaje = aciertos/len(categorias_estimadas)

    res = 'El porcentaje de acierto es: '+str(porcentaje*100)+' %'
    print(res)
    return res

def testear_noticia(k,ruta_noticia_test):
    def numeros_a_categorias(numero):
        switcher = {
            "0": "Cultura",
            "1": "Sociedad",
            "2": "Deporte",
            "3": "Tecnologia",
            "4": "Economia",
            "5": "Ciencia"
        }
        return switcher.get(numero, "Ninguna")

    # Cargar las palabras clave y los datos producidos en el entrenamiento del modelo
    palabras_clave = ha.leer_palabras_clave(ruta_palabras_clave)
    conjunto_entrenamiento = ha.cargar_entrenamiento(ruta_archivo_entrenamiento)

    if int(k)>len(conjunto_entrenamiento):
        print('El k es demasiado grande, no puede ser mayor que ',len(conjunto_entrenamiento))
        return -1

    # Asignar a cada vector de pesos de una noticia su categoría correspondiente
    ha.cargar_categorias(ruta_categorias, conjunto_entrenamiento)

    #Leer una noticia de prueba desde un archivo
    noticia_test = ha.leer_noticia(ruta_noticia_test)

    #Contar las apariciones de palabras clave en la noticia cargada
    apariciones = ha.palabras_clave_noticia(noticia_test, palabras_clave)

    # Cargar las frecuencias documentales inversas
    f_docs_inv = ha.cargar_frecuencias_documentales_inversas(ruta_archivo_f_doc)

    # Calcular los pesos
    pesos = [apariciones[i] * f_docs_inv[i] for i in range(len(f_docs_inv))]

    #Escoger los vecinos de la noticia de prueba
    vecinos = knn.escoger_vecinos(conjunto_entrenamiento, pesos,int(k))

    #A partir de los vecinos más cercanos, sacar la categoría estimada del documento
    categoria_del_documento, = Counter(vecinos).most_common(1)

    categoria = numeros_a_categorias(categoria_del_documento[0])
    
    respuesta ='La categoría estimada del documento evaluado es:  '+categoria
    print(respuesta)
    
    return respuesta
    
    
    
