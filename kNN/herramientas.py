import string
import re
import numpy
import csv
import copy
from sklearn import model_selection


def categorizar_noticias(noticias,categorias):
    resultado = copy.deepcopy(noticias)
    for i  in range(len(noticias)):
        resultado[i].append(categorias[i])
    return resultado

def dividir_noticias(noticias_categorizadas,ratio_noticias_entrenamiento):
    noticias_test, noticias_entrenamiento = model_selection.train_test_split(
        noticias_categorizadas, test_size=ratio_noticias_entrenamiento, random_state=123456)
    return [noticias_entrenamiento, noticias_test]

def cargar_entrenamiento(path):
    archivo = open(path, 'r', encoding='utf8')
    datos_cargados = archivo.readlines()
    archivo.close()
    datos_cargados_float = []
    resultado =[]
    for i in range(len(datos_cargados)):
        string_sin_saltos_de_linea = datos_cargados[i].strip()
        temp= string_sin_saltos_de_linea.split(',')
        datos_float = [float(numero) for numero in temp]
        datos_cargados_float.append(datos_float)
    for columna in range(len(datos_cargados_float[0])):
        pesos_noticia =[]
        for fila in range(len(datos_cargados_float)):
            pesos_noticia.append(datos_cargados_float[fila][columna])
        resultado.append(pesos_noticia)
    return resultado


def cargar_categorias(path,matriz_entrenamiento):
    archivo = open(path, 'r',encoding='utf8')
    categorias = archivo.read().lower().splitlines()
    archivo.close()
    resultado =[]
    for i in range(len(matriz_entrenamiento)):
        a=matriz_entrenamiento[i]
        b=categorias[i]
        a.append(b)
        resultado.append(a)
    return resultado




def leer_categorias(path):
    file = open(path, 'r',encoding="utf8")
    keywords = file.read().lower().splitlines()
    file.close()
    return keywords


def leer_palabras_clave(path):
    file = open(path, 'r',encoding="utf8")
    keywords = file.read().lower().splitlines()
    file.close()
    return keywords



def leer_noticia(path):
    file = open(path,'r',encoding="utf8")
    announcement = file.readlines()
    file.close()
    noticia_array = announcement[0].split(' ')
    return noticia_array


def leer_noticias_entrenamiento(path):
    file = open(path, 'r', encoding="utf-8")
    input_announcements = file.readlines()
    file.close()
    announcement_list = []
    for announcement in input_announcements:
        a = announcement.split(",")
        announcement_list.append(a)
    return announcement_list


def leer_multiples_noticias(path):
    file = open(path,'r',encoding="utf8")
    input_announcements = file.readlines()
    file.close()
    whitelist = string.ascii_letters + ' ' + 'á' + 'é' + 'í' + 'ó' + 'ú' + 'ñ'
    announcement_list = []
    for announcement in input_announcements:
        announcement_str = ''
        for char in announcement:
            if char in whitelist:
                announcement_str += char.lower()
        a = re.sub ("[^\w]", " ", announcement_str).split()
        announcement_list.append(a)
    return announcement_list


def palabras_clave_noticia(announcement,keywords):
    keywords_counter = numpy.zeros(len(keywords), dtype=int)
    for word in announcement:
        if word in keywords:
            keywords_counter[keywords.index(word)] += 1
    return keywords_counter


def palabras_clave_multiples_noticias(announcements,keywords,categories):
    counters = []
    for i in range(len(announcements)):
        keywords_counter = numpy.zeros(len(keywords), dtype=int)
        for word in announcements[i]:
            if word in keywords:
                keywords_counter[keywords.index(word)] += 1
        keywords_counter[len(keywords_counter)-1] = categories[i]
        counters.append(keywords_counter.tolist())
    return counters

def guardar_frecuencias_documentales_inversas(f_documentales,ruta):
    with open(ruta, 'w') as out:
        for frec in f_documentales:
            out.write(str(frec) + '\n')

def cargar_frecuencias_documentales_inversas(ruta):
    file = open(ruta, 'r', encoding="utf8")
    frecs = file.read().splitlines()
    file.close()
    results = list(map(float, frecs))
    return results

def guardar_pesos(data, path):
    with open(path, "w", encoding='utf-8') as csv_file:

        writer = csv.writer(csv_file, delimiter=',', dialect='unix', quoting=csv.QUOTE_NONE)

        for line in data:
            writer.writerow(line)

def guardar_noticias_entrenamiento_test(noticias_entrenamiento,noticias_test,ruta_not_entr,ruta_cat_entr,ruta_not_test,ruta_cat_test):

    n_entr = copy.deepcopy(noticias_entrenamiento)
    n_test = copy.deepcopy(noticias_test)

    res_entr = 'El número de noticias de entrenamiento es: '+ str(len(n_entr))
    res_test =  'El número de noticias de test es: '+ str(len(n_test))

    categorias_entrenamiento = []
    for noticia_entr in n_entr:
        categorias_entrenamiento.append(noticia_entr[-1])
        del noticia_entr[-1]

    categorias_test = []
    for noticia_test in n_test:
        categorias_test.append(noticia_test[-1])
        del noticia_test[-1]

    archivo_noticias_entrenamiento = open(ruta_not_entr, "w",newline='', encoding='utf-8')
    writer1 = csv.writer(archivo_noticias_entrenamiento, delimiter=',')

    for linea_n_e in n_entr:
        writer1.writerow(linea_n_e)
    archivo_noticias_entrenamiento.close()

    with open(ruta_cat_entr, 'w') as out:
        for cat in categorias_entrenamiento:
            out.write(cat + '\n')

    archivo_noticias_test = open(ruta_not_test, "w",newline='', encoding='utf-8')
    writer3 = csv.writer(archivo_noticias_test, delimiter=',')

    for linea_n_t in n_test:
        writer3.writerow(linea_n_t)
    archivo_noticias_test.close()

    with open(ruta_cat_test, 'w') as out:
        for cat in categorias_test:
            out.write(cat + '\n')

    res = res_entr+'\n'+res_test
    return res