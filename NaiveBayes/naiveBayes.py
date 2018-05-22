import math
import numpy as np
from pandas import DataFrame
from sklearn import model_selection
import string, re, csv
import copy

# UTILES PARA LECTURA DE NOTICIAS------------------------------------------------------

def read_single_announcement(path):
    file = open(path,'r',encoding="utf8")
    announcement = file.readlines()
    file.close()
    noticia_array = announcement[0].split(' ')
    return noticia_array

def keyword_number_of_single_new(announcement,keywords):
    keywords_counter = np.zeros(len(keywords), dtype=int)
    for word in announcement:
        if word in keywords:
            keywords_counter[keywords.index(word)] += 1
    return keywords_counter

def readNews(news_path, keywords_path, categories_path):
    news = read_announcements(news_path)
    keywords = read_keywords(keywords_path)
    categories = read_categories(categories_path)
    results = keyword_number_of_multiple_news(news, keywords, categories)
    return [results, keywords]


def read_announcements(path):
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


def read_categories(path):
    file = open(path, 'r',encoding="utf8")
    categories = file.read().lower().splitlines()
    file.close()
    return categories


def read_keywords(path):
    file = open(path, 'r',encoding="utf8")
    keywords = file.read().lower().splitlines()
    file.close()
    keywords.append('category')
    return keywords


def keyword_number_of_multiple_news(announcements,keywords,categories):
    counters = []
    i=0
    for announcement in announcements:
        keywords_counter = np.zeros(len(keywords), dtype=int)
        for word in announcement:
            if word in keywords:
                keywords_counter[keywords.index(word)] += 1
        keywords_counter[len(keywords_counter)-1] = categories[i]
        counters.append(keywords_counter)
        i+=1
    return counters


def diccionarioCat(x):
    return {
        0: "Cultura",
        2: "Deportes",
        3: "Tecnología",
        4: "Economía",
        5: "Ciencia",
    }.get(x, "Sociedad")

def diccionarioFiles(x):
    return {
        "Cultura": "archivos/test_cultura.txt",
        "Deportes": "archivos/test_deporte.txt",
        "Tecnología": "archivos/test_tecnologia.txt",
        "Economía": "archivos/test_economia.txt",
        "Ciencia": "archivos/test_ciencia.txt",
        "Sociedad": "archivos/test_sociedad.txt",
        "Desconocida": "archivos/test_usuario.txt"
    }.get(x, None)

# CREACIÓN DEL ENTRENAMIENTO-----------------------------------------------------------------

def splitDataset(dataset, splitRatio,keywords):
    data = DataFrame(dataset, columns=keywords)
    copy, trainSet = model_selection.train_test_split(
    data, test_size=splitRatio, random_state=12348,
    stratify=data['category'])
    trainSet=trainSet.values.tolist()
    copy=copy.values.tolist()
    for i in range(len(trainSet)):
        trainSet[i] = [float(x) for x in trainSet[i]]
    for i in range(len(copy)):
        copy[i] = [float(x) for x in copy[i]]
    return [trainSet, copy]


def getCategories(trainingSet):
    result=[]
    for i in trainingSet:
        result.append(i[-1])
    result=list(set(result))
    return result


def calculatorPc(summaries, trainingSet):
    apariciones= [0 for i in range(len(summaries))]
    for i in trainingSet:
        categoria = i[-1]
        apariciones[int(categoria)] += 1
    pc = [apariciones[i]/len(trainingSet) for i in range(len(summaries))]
    return pc


def calculatorPtc(summaries, trainingSet, keywords):
    apariciones = [[0 for j in range(len(keywords)-1)] for i in range(len(summaries))]
    totales= [0 for i in range(len(summaries))]
    for i in trainingSet:
        keyword=0
        for j in i:
            if keyword < len(apariciones[int(i[-1])]):
                apariciones[int(i[-1])][keyword] += j
                totales[int(i[-1])] += 1
            keyword+=1
    ptc = [[(apariciones[i][j]+1)/(totales[i]+len(keywords)) for j in range(len(keywords)-1)] for i in range(len(summaries))]
    return ptc


def training_NB_writer(pc, ptc, path):
    with open(path, "w") as csv_file:

        writer = csv.writer(csv_file, delimiter=',')

        writer.writerow(pc)
        for i in ptc:
            writer.writerow(i)


def prepareTrainingSet(trainingSet, keywords):
    categories = getCategories(trainingSet)
    pc = calculatorPc(categories, trainingSet)
    ptc = calculatorPtc(categories, trainingSet, keywords)

    training_NB_writer(pc, ptc, 'entrenamiento_NB')


#LECTURA DEL ARCHIVO EN QUE SE ALMACENA EL ENTRENAMIENTO Y PRUEBA


def load_training_NB(filename):
    lines = csv.reader(open(filename, "r"))
    ptc=[]
    dataset = list(lines)
    pc = dataset.pop(0)
    pc = [float(i) for i in pc]
    dataset.pop(0)
    for z in range(len(dataset)):
        if z%2 ==0:
            ptc.append(dataset[z])
    for z in range(len(ptc)):
        ptc[z] = [float(j) for j in ptc[z]]

    return [pc, ptc]


def getPredictions(pc, ptc, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(pc, ptc, testSet[i])
        predictions.append(result)
    return predictions

def predict(pc, ptc, inputVector):
    probabilities = calculatorPTotal(pc, ptc, inputVector)
    bestLabel, bestProb = None, -1
    for i in range(len(probabilities)):
        if bestLabel is None or probabilities[i] > bestProb:
            bestProb = probabilities[i]
            bestLabel = i
    return bestLabel

def predict2(pc, ptc, inputVector):
    probabilities = calculatorPTotal(pc, ptc, inputVector)
    bestLabel, bestProb = None, -1
    for i in range(len(probabilities)):
        if bestLabel is None or probabilities[i] > bestProb:
            bestProb = probabilities[i]
            bestLabel = i
    return diccionarioCat(bestLabel)

def calculatorPTotal(pc,ptc,inputVector):
    pTotal=[0 for i in range(len(pc))]
    copyptc=copy.deepcopy(ptc)
    for i in range(len(pTotal)):
        for j in range(len(inputVector)-1):
            copyptc[i][j]=math.pow(ptc[i][j],inputVector[j])
        pTotal[i] += pc[i]*np.prod(copyptc[i])
    return pTotal


def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0