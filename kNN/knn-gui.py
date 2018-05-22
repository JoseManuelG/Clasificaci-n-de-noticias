import sys
import dividir_noticias
import entrenar_modelo
import testear_modelo
import herramientas as ha
from PyQt5.QtWidgets import (QMainWindow, QPushButton,QTabWidget,
                            QWidget, QLCDNumber, QSlider,QVBoxLayout, QApplication, QSpinBox, QMessageBox)
from PyQt5.QtCore import Qt

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Clasficación de documentos, algoritmo kNN'
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
        res = dividir_noticias.divide(ratio)
        self.statusBar().showMessage(res)
        QMessageBox.about(self, 'División de noticias',res)

    def buttonClicked2(self):
        res = entrenar_modelo.entrenar()
        self.statusBar().showMessage("Modelo entrenado con "+res+" noticias.")
        QMessageBox.about(self,'Entrenamiento de modelo',"Modelo entrenado con "+res+" noticias.")

    def buttonClicked3(self,k):
        conjunto_entrenamiento = ha.cargar_entrenamiento("archivos/entrenamiento.csv")
        if(k>len(conjunto_entrenamiento)):
             QMessageBox.about(self,'ERROR',"El k debe ser menor o igual a "+str(len(conjunto_entrenamiento))+" para este modelo.")
        else:
            res = testear_modelo.testear_multiples_noticias(k)
            self.statusBar().showMessage(res)
            QMessageBox.about(self,'Categorizar noticias de prueba',res)

    def buttonClickedCategory(self,k,ruta):
        conjunto_entrenamiento = ha.cargar_entrenamiento("archivos/entrenamiento.csv")
        if(k>len(conjunto_entrenamiento)):
             QMessageBox.about(self,'ERROR',"El k debe ser menor o igual a "+str(len(conjunto_entrenamiento))+" para este modelo.")
        else:
            res = testear_modelo.testear_noticia(k,ruta)
            self.statusBar().showMessage(res)
            QMessageBox.about(self,'Categorizar una noticia',res)

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

        # Inicializacion de elementos de la ventana
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(700, 500)
        self.lcd = QLCDNumber()
        self.sld = QSlider(Qt.Horizontal)
        self.sld.setMinimum(1)

        # Anadir pestanas a la ventana
        self.tabs.addTab(self.tab1, "División de noticias para entrenamiento")
        self.tabs.addTab(self.tab2, "Entrenar el modelo")
        self.tabs.addTab(self.tab3, "Categorizar noticias de prueba")
        self.tabs.addTab(self.tab4, "Categorizar una noticia")

        # Primera pestana
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("Dividir noticias!",self)
        self.pushButton1.setToolTip("Pulsa para dividir las noticias en dos conjuntos, uno de entrenamiento y otro de prueba")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)
        self.pushButton1.clicked.connect(lambda: parent.buttonClicked1(self.sld.value()/100))
        self.tab1.layout.addWidget(self.lcd)
        self.tab1.layout.addWidget(self.sld)
        self.tab1.setLayout(self.tab1.layout)
        self.sld.valueChanged.connect(self.lcd.display)
        self.tab1.setGeometry(300, 300, 250, 150)
        self.show()

        # Segunda pestana
        self.tab2.layout = QVBoxLayout(self)
        self.pushButton2 = QPushButton("Entrenar modelo!")
        self.pushButton2.setToolTip("Pulsa para crear un modelo estadístico a partir de las palabras clave y las categorías de las noticias de entrenamiento")
        self.tab2.layout.addWidget(self.pushButton2)
        self.tab2.setLayout(self.tab2.layout)
        self.pushButton2.clicked.connect(parent.buttonClicked2)

        # Tercera pestana
        self.tab3.layout = QVBoxLayout(self)
        
        self.numberInput1 = QSpinBox(self)
        self.numberInput1.setToolTip("Introduce el número de vecinos con los que se podrá comparar cada noticia para establecer su categoría")
        self.numberInput1.setRange(1,100)
        self.numberInput1.setAlignment(Qt.AlignBottom)
        self.tab3.layout.addWidget(self.numberInput1)
        
        self.pushButton3 = QPushButton("Categorizar múltiples noticias!")
        self.pushButton3.setToolTip("Usa el modelo de entrenamiento para pronosticar las categorías de las noticias de prueba")
        self.tab3.layout.addWidget(self.pushButton3)
        self.tab3.setLayout(self.tab3.layout)
        self.pushButton3.clicked.connect(lambda: parent.buttonClicked3(self.numberInput1.value()))

        # Cuarta pestana
        self.tab4.layout = QVBoxLayout(self)
        self.numberInput2 = QSpinBox(self)
        self.numberInput2.setToolTip("Introduce el número de vecinos con los que se podrá comparar cada noticia para establecer su categoría")
        self.numberInput2.setRange(1,100)
        self.tab4.layout.addWidget(self.numberInput2)
    
        self.pushButton4 = QPushButton("Categorizar noticia de cultura!")
        self.pushButton4.setToolTip("Pronostica la categoría de un documento de cultura")
        self.tab4.layout.addWidget(self.pushButton4)
        self.pushButton4.clicked.connect(lambda: parent.buttonClickedCategory(self.numberInput2.value(),'archivos/test_cultura.csv'))
        
        self.pushButton5 = QPushButton("Categorizar noticia de sociedad!")
        self.pushButton5.setToolTip("Pronostica la categoría de un documento de sociedad")
        self.tab4.layout.addWidget(self.pushButton5)
        self.pushButton5.clicked.connect(lambda: parent.buttonClickedCategory(self.numberInput2.value(),'archivos/test_sociedad.csv'))
        
        self.pushButton6 = QPushButton("Categorizar noticia de deporte!")
        self.pushButton6.setToolTip("Pronostica la categoría de un documento de deporte")
        self.tab4.layout.addWidget(self.pushButton6)
        self.pushButton6.clicked.connect(lambda: parent.buttonClickedCategory(self.numberInput2.value(),'archivos/test_deporte.csv'))
        
        self.pushButton7 = QPushButton("Categorizar noticia de tecnología!")
        self.pushButton7.setToolTip("Pronostica la categoría de un documento de tecnología")
        self.tab4.layout.addWidget(self.pushButton7)
        self.pushButton7.clicked.connect(lambda: parent.buttonClickedCategory(self.numberInput2.value(),'archivos/test_tecnologia.csv'))
        
        self.pushButton8 = QPushButton("Categorizar noticia de economía!")
        self.pushButton8.setToolTip("Pronostica la categoría de un documento de economía")
        self.tab4.layout.addWidget(self.pushButton8)
        self.pushButton8.clicked.connect(lambda: parent.buttonClickedCategory(self.numberInput2.value(),'archivos/test_economia.csv'))
        
        self.pushButton9 = QPushButton("Categorizar noticia de ciencia!")
        self.pushButton9.setToolTip("Pronostica la categoría de un documento de ciencia")
        self.tab4.layout.addWidget(self.pushButton9)
        self.tab4.setLayout(self.tab4.layout)
        self.pushButton9.clicked.connect(lambda: parent.buttonClickedCategory(self.numberInput2.value(),'archivos/test_ciencia.csv'))

        self.pushButton10 = QPushButton("Categorizar noticia de categoría desconocida!")
        self.pushButton10.setToolTip("Pronostica la categoría de un documento del que no se sabe la categoría")
        self.tab4.layout.addWidget(self.pushButton10)
        self.tab4.setLayout(self.tab4.layout)
        self.pushButton10.clicked.connect(lambda: parent.buttonClickedCategory(self.numberInput2.value(), 'archivos/test_usuario.csv'))

        # Anadir pestanas al widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())