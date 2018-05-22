import numpy as np
import math


def frecuencia_de_terminos_en_documentos(documentos,terminos):
    matriz = []
    for termino in terminos:
        apariciones_en_documentos = []
        for documento in documentos:
            apariciones_en_documentos.append(documento.count(termino))
        matriz.append(apariciones_en_documentos)
    return matriz

def frecuencias_documentales(documentos,terminos):
    resultados = []
    for termino in terminos:
        n_documentos = 0
        for documento in documentos:
            if termino in documento:
                n_documentos += 1
        resultados.append(n_documentos)
    return resultados

def frecuencias_documentales_inversas(total_keywords,total_news,f_docs):
    resultados = []
    for i in range(total_keywords):
        res = 0
        if f_docs[i] != 0:
            res = math.log10(total_news/f_docs[i])
        resultados.append(res)
    return resultados

def  pesos_de_terminos_en_documentos(frecuencias,frecuencias_inversas):
    resultados =[]
    for i in range(len(frecuencias)):
        pesos_de_termino =[]
        for j in range(len(frecuencias[0])):
            pesos_de_termino.append((frecuencias[i][j])*frecuencias_inversas[i])
        resultados.append(pesos_de_termino)
    return resultados

def calcular_distancia(vector1,vector2):
    producto_escalar = np.dot(vector1, vector2)
    modulo_vector_a = np.linalg.norm(vector1)
    modulo_vector_b = np.linalg.norm(vector2)
    result =0
    if (modulo_vector_a * modulo_vector_b) != 0:
        result = producto_escalar / (modulo_vector_a * modulo_vector_b)
    return result

def escoger_vecinos(pesos_documentos_entrenamiento, pesos_documento_test , k):
    distancias = []
    for pesos_documento in pesos_documentos_entrenamiento:
        distancia = calcular_distancia(pesos_documento_test,pesos_documento[:-1])
        distancias.append((distancia,pesos_documento))
    distancias.sort(reverse=True)
    vecinos = []
    for i in range(k):
        vecinos.append(distancias[i][1][-1])
    return vecinos

