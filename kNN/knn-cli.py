# -*- coding: utf-8 -*-
#!usr/bin/python
import argparse
import sys
import dividir_noticias
import entrenar_modelo
import testear_modelo

#Definición de los argumentos que puede recibir el programa
parser = argparse.ArgumentParser()
parser.add_argument("-d","--dividir", help="Indica si se quiere dividir el conjunto de entrenamiento",action="store_true")
parser.add_argument("-r","--ratio", help="Establece el ratio de noticias que se usaran para entrenamiento, por defecto se cogeran todas.")
parser.add_argument("-e","--entrenar",help="Entrena el modelo a partir de los archivos de noticias y categorias pasados",action="store_true")
parser.add_argument("-k","--k_vecinos", help="Indica con cuantos vecinos se comparara una noticia")
parser.add_argument("-t","--testear_noticia",help="Estima la categoria de un documento dado")
parser.add_argument("-tn","--testear_multiples_noticias",help="Estima las categorias de varios documentos a la vez",action="store_true")
args = parser.parse_args()

a = len(sys.argv)

#Restricciones de argumentos a recibir y llamadas a funcionalidades
if len(sys.argv) == 1:
    print('Este programa necesita parametros para funcionar, para mas informacion, utiliza el parametro -h')

elif args.ratio and args.dividir and len(sys.argv) == 4 and not args.entrenar and not args.k_vecinos and not args.testear_noticia and not args.testear_multiples_noticias:
    if 0 < float(args.ratio) < 1:
        dividir_noticias.divide(float(args.ratio))
    else:
        print('El ratio de division de documentos debe ser un numero mayor que cero(0) y menor que uno(1)')
elif args.entrenar and len(sys.argv) == 2:
    entrenar_modelo.entrenar()
elif args.dividir and len(sys.argv) == 2:
    dividir_noticias.divide(0.99999)
elif args.k_vecinos and args.testear_noticia and len(sys.argv) == 5 and not args.dividir and not args.ratio and not args.entrenar and not args.testear_multiples_noticias:
    testear_modelo.testear_noticia(args.k_vecinos,args.testear_noticia)
elif args.k_vecinos and args.testear_multiples_noticias and len(sys.argv) == 4 and not args.dividir and not args.ratio and not args.entrenar and not args.testear_noticia:
    if 0 < float(args.k_vecinos) :
        testear_modelo.testear_multiples_noticias(args.k_vecinos)
    else:
        print("El parametro k debe ser mayor que cero(0).")
else:
    print('Combinacion erronea de parametros. Consulte el manual para obtener ayuda.')



