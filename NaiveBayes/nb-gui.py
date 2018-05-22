import sys
import naiveBayes as nb
from PyQt5.QtWidgets import (QMainWindow, QPushButton,QTabWidget,QInputDialog,
                            QWidget, QLCDNumber, QSlider,QVBoxLayout, QApplication, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.testSet = None
        self.trainingSet = None
        self.categories = None
        self.keywords = None
        self.log = ""
        self.sCat = ""
        self.title = 'Clasficación de documentos, algoritmo Naive Bayes'
        self.left = 300
        self.top = 150
        self.width = 700
        self.height = 500
        self.statusBar()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()
    def buttonClicked1(self,ratio):
        if(ratio<0.05):
            QMessageBox.about(self,"ERROR","El porcentaje de noticias debe ser superior al 5%")
        else:
            results,self.keywords = nb.readNews('archivos/news.txt', 'archivos/keywords.txt', 'archivos/categorias.txt')
            self.trainingSet, self.testSet = nb.splitDataset(results, ratio, self.keywords)
            self.statusBar().showMessage("Conjunto de entrenamiento: " + str(len(self.trainingSet)) +
                                         " Conjunto de pruebas: "+ str(len(self.testSet)))
            QMessageBox.about(self, "División", "-Conjunto de entrenamiento: " + str(len(self.trainingSet)) +
                              " noticias\n-Conjunto de pruebas: "+ str(len(self.testSet))+" noticias")

    def buttonClicked2(self):
        if self.trainingSet == None:
            QMessageBox.about(self,"ERROR","Debe dividir el conjunto de noticias antes de entrenar.")
        else:
            nb.prepareTrainingSet(self.trainingSet, self.keywords)
            self.statusBar().showMessage("Modelo entrenado con " + str(len(self.trainingSet)) + " noticias")
            QMessageBox.about(self, "Entrenado!", "-El modelo ha sido entrenado con: " + str(len(self.trainingSet))+" noticias")

    def buttonClicked3(self):
        if(self.testSet == None):
            QMessageBox.about(self, "ERROR", "Ha de seleccionar la división de noticias para prueba")
        else:
            pc, ptc = nb.load_training_NB('entrenamiento_NB')
            predictions = nb.getPredictions(pc, ptc, self.testSet)
            accuracy = nb.getAccuracy(self.testSet, predictions)
            self.statusBar().showMessage('El porcentaje de aciertos es: ' + str(accuracy) + '%')
            QMessageBox.about(self, "RESULTADO", 'El porcentaje de aciertos es del ' + str(accuracy) + '% \ncon '+ str(len(self.trainingSet))+ ' noticias de entrenamiento \ny '+ str(len(self.testSet))+' noticias de prueba.')

    def unitario(self,path):
        noticia = nb.read_single_announcement(path)
        self.keywords = nb.read_keywords('archivos/keywords.txt')
        test = nb.keyword_number_of_single_new(noticia, self.keywords)
        pc, ptc = nb.load_training_NB('entrenamiento_NB')
        cat = nb.predict2(pc, ptc, test)
        self.statusBar().showMessage('Su noticia es de la categoria: ' + str(cat))
        QMessageBox.about(self, "RESULTADO", "Su noticia es de la categoria "+str(cat) + ". ")

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer", "Percentage:", 28, 0, 100, 1)
        if okPressed:
            print(i)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Salir del programa',
                                     "¿Está seguro de salir?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Inicialización de elementos de la ventana
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(700, 500)
        self.lcd = QLCDNumber()
        self.sld = QSlider(Qt.Horizontal)
        self.sld.setMaximum(94)

        # Anadir pestañas a la ventana
        self.tabs.addTab(self.tab1, "División de noticias y entrenamiento")
        self.tabs.addTab(self.tab3, "Categorizar múltiples noticias")
        self.tabs.addTab(self.tab4, "Categorizar una noticia")

        # Primera pestana
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("Dividir el conjunto de noticias de entrenamiento y prueba: ",self)
        self.tab1.layout.addWidget(self.pushButton1)
        self.pushButton1.clicked.connect(lambda: parent.buttonClicked1(self.sld.value()/100))
        self.pushButton2 = QPushButton("Entrenar el modelo con la división seleccionada: ", self)
        self.tab1.layout.addWidget(self.pushButton2)
        self.tab1.setLayout(self.tab1.layout)
        self.pushButton2.clicked.connect(lambda: parent.buttonClicked2())
        self.tab1.layout.addWidget(self.lcd)
        self.tab1.layout.addWidget(self.sld)
        self.tab1.setLayout(self.tab1.layout)
        self.sld.valueChanged.connect(self.lcd.display)
        self.tab1.setGeometry(300, 300, 250, 150)
        self.show()

        # Segunda pestana
        self.tab3.layout = QVBoxLayout(self)
        self.pushButton3 = QPushButton("Extraer el porcentaje de aciertos frente al conjunto de prueba")
        self.tab3.layout.addWidget(self.pushButton3)
        self.tab3.setLayout(self.tab3.layout)
        self.pushButton3.clicked.connect(lambda: parent.buttonClicked3())

        # Tercera pestana
        self.tab4.layout = QVBoxLayout(self)
        self.pushCiencia = QPushButton("Categorizar noticia de Ciencia")
        self.tab4.layout.addWidget(self.pushCiencia)
        self.pushCiencia.clicked.connect(lambda: parent.unitario("archivos/test_ciencia.txt"))

        self.pushSociedad = QPushButton("Categorizar noticia de Sociedad")
        self.tab4.layout.addWidget(self.pushSociedad)
        self.pushSociedad.clicked.connect(lambda: parent.unitario("archivos/test_sociedad.txt"))

        self.pushEconomia = QPushButton("Categorizar noticia de Economia")
        self.tab4.layout.addWidget(self.pushEconomia)
        self.pushEconomia.clicked.connect(lambda: parent.unitario("archivos/test_economia.txt"))

        self.pushDeportes = QPushButton("Categorizar noticia de Deportes")
        self.tab4.layout.addWidget(self.pushDeportes)
        self.pushDeportes.clicked.connect(lambda: parent.unitario("archivos/test_deporte.txt"))

        self.pushCultura = QPushButton("Categorizar noticia de Cultura")
        self.tab4.layout.addWidget(self.pushCultura)
        self.pushCultura.clicked.connect(lambda: parent.unitario("archivos/test_cultura.txt"))

        self.pushTecnoligia = QPushButton("Categorizar noticia Tecnoligia")
        self.tab4.layout.addWidget(self.pushTecnoligia)
        self.pushTecnoligia.clicked.connect(lambda: parent.unitario("archivos/test_tecnologia.txt"))

        self.pushUsuario = QPushButton("Categorizar noticia Desconocida")
        self.tab4.layout.addWidget(self.pushUsuario)
        self.tab4.setLayout(self.tab4.layout)
        self.pushUsuario.clicked.connect(lambda: parent.unitario("archivos/test_usuario.txt"))

        # Añadir pestañas al widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())