import argparse
import sys
import naiveBayes as nb

if len(sys.argv) ==1:
    print('Este programa necesita parámetros para funcionar, para más información, utiliza el parámetro -h')

parser = argparse.ArgumentParser()
parser.add_argument("-p","--porcentaje", help="Establece el porcentaje de noticias que se usaran para entrenamiento o testeo, por defecto se cogera el 0.67")
parser.add_argument("-e","--entrenar",help="Entrena el modelo a partir de los archivos de noticias y categorias pasados",action="store_true")
parser.add_argument("-t","--testear_noticia",help="Estima la categoria de un documento dado segun el nombre de la categoria")
parser.add_argument("-tn","--testear_multiples_noticias",help="Estima las categorias de varios documentos a la vez",action="store_true")
args = parser.parse_args()



if args.porcentaje and args.entrenar and not args.testear_noticia and not args.testear_multiples_noticias:
    news = nb.read_announcements('archivos/news.txt')
    keywords = nb.read_keywords('archivos/keywords.txt')
    categorias = nb.read_categories('archivos/categorias.txt')
    results = nb.keyword_number_of_multiple_news(news, keywords, categorias)
    trainingSet, testSet = nb.splitDataset(results, float(args.porcentaje), keywords)
    nb.prepareTrainingSet(trainingSet, keywords)
    print("El modelo ha sido entrenado con "+str(len(trainingSet))+" noticias.")

elif args.entrenar and not args.porcentaje and not args.testear_noticia and not args.testear_multiples_noticias:
    news = nb.read_announcements('archivos/news.txt')
    keywords = nb.read_keywords('archivos/keywords.txt')
    categorias = nb.read_categories('archivos/categorias.txt')
    results = nb.keyword_number_of_multiple_news(news, keywords, categorias)
    trainingSet, testSet = nb.splitDataset(results, 0.67, keywords)
    nb.prepareTrainingSet(trainingSet, keywords)
    print("El modelo ha sido entrenado con el 67% de las noticias por defecto.")

elif args.testear_noticia and not args.entrenar and not args.porcentaje and not args.testear_multiples_noticias:
    path = nb.diccionarioFiles(args.testear_noticia)
    if(path != None):
        noticia = nb.read_single_announcement(path)
        keywords = nb.read_keywords('archivos/keywords.txt')
        test = nb.keyword_number_of_single_new(noticia, keywords)
        pc, ptc = nb.load_training_NB('entrenamiento_NB')
        print("Su noticia es de "+nb.predict2(pc, ptc, test)+"!!")
    else:
        print("ERROR: CATEGORIA NO ENCONTRADA")

elif args.porcentaje and args.testear_multiples_noticias and not args.testear_noticia and not args.entrenar:
    news = nb.read_announcements('archivos/news.txt')
    keywords = nb.read_keywords('archivos/keywords.txt')
    categorias = nb.read_categories('archivos/categorias.txt')
    results = nb.keyword_number_of_multiple_news(news, keywords, categorias)
    trainSet, testSet = nb.splitDataset(results, 1-float(args.porcentaje), keywords)
    pc, ptc = nb.load_training_NB('entrenamiento_NB')
    predictions = nb.getPredictions(pc, ptc, testSet)
    accuracy = nb.getAccuracy(testSet, predictions)
    print('Porcentaje de aciertos: ' + str(accuracy) + '% contra '+str(len(testSet))+' noticias de prueba')

elif args.testear_multiples_noticias and not args.porcentaje and not args.testear_noticia and not args.entrenar:
    news = nb.read_announcements('archivos/news.txt')
    keywords = nb.read_keywords('archivos/keywords.txt')
    categorias = nb.read_categories('archivos/categorias.txt')
    results = nb.keyword_number_of_multiple_news(news, keywords, categorias)
    trainSet, testSet = nb.splitDataset(results, 0.05, keywords)
    pc, ptc = nb.load_training_NB('entrenamiento_NB')
    predictions = nb.getPredictions(pc, ptc, testSet)
    accuracy = nb.getAccuracy(testSet, predictions)
    print('Porcentaje de aciertos: ' + str(accuracy) + '% contra '+str(len(testSet))+' noticias de prueba')

else:
    print("COMANDO NO ENCONTRADO")