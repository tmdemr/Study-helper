import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog
from py_rc import passowrd_rc, user_rc, user_profile_rc, login_rc
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
import pymysql

conn = pymysql.connect(host='localhost',
                           user='pi',
                           password='raspberry',
                           db='suppoter',
                           charset='utf8')

class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            #print("Viewer Dropped frame!")
            pass

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 480)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 457, 801, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(0, 437, 801, 23))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setInvertedAppearance(False)
        self.progressBar_2.setObjectName("progressBar_2")
        #self.id = ''
        #
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(610, 0, 181, 131))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(105, 80, 71, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(5, 80, 91, 31))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(5, 40, 101, 31))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(105, 40, 71, 31))
        self.comboBox.setObjectName("comboBox")
        #self.id_edit.textChanged.connect(id_editFunc)
        #self.id_edit.setGeometry(QtCore.QRect(105, 40, 71, 31))
        #self.btn_input_id.clicked.connect(self.input_id)
        #self.btn_input.setGeometry(QtCore.QRect(105, 40, 71, 41))

        #
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(610, 140, 181, 131))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_3.setGeometry(QtCore.QRect(105, 80, 71, 31))
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(5, 80, 100, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(5, 40, 111, 31))
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setObjectName("label_4")
        self.comboBox_4 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_4.setGeometry(QtCore.QRect(105, 40, 71, 31))
        self.comboBox_4.setObjectName("comboBox_4")
        #
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(610, 280, 181, 90))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.radio = QtWidgets.QRadioButton("Camera", self.groupBox_3)
        self.radio.setGeometry(QtCore.QRect(10, 30, 130, 20))
        self.radio.setObjectName("radio")
        self.radio.setChecked(True)
        self.radio_2 = QtWidgets.QRadioButton("File", self.groupBox_3)
        self.radio_2.setGeometry(QtCore.QRect(10, 60, 130, 20))
        self.radio_2.setObjectName("radio_2")
        
        self.push_button1 = QtWidgets.QPushButton('Start',self.centralwidget)
        self.push_button1.setGeometry(QtCore.QRect(610, 385, 85, 40))
        self.push_button1.setObjectName("Start")
        self.push_button2 = QtWidgets.QPushButton('Quit', self.centralwidget)
        self.push_button2.setGeometry(QtCore.QRect(710, 385, 85, 40))
        self.push_button2.setObjectName("Quit")
        self.image_viewer1 = ImageViewer(self.centralwidget)
        self.image_viewer1.hide()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Anti-Sleepiness"))
        self.centralwidget.setStyleSheet("QWidget {background-color: #FFFFFF }")
        self.groupBox.setTitle(_translate("MainWindow", "조건길이"))
        self.label_2.setText(_translate("MainWindow", "조건2(sec)"))
        self.label.setText(_translate("MainWindow", "조건1(sec)"))
        
        self.groupBox_2.setTitle(_translate("MainWindow", "민감도"))
        self.label_3.setText(_translate("MainWindow", "감음(Ratio)"))
        self.label_4.setText(_translate("MainWindow", "(%)"))
        self.groupBox_3.setTitle(_translate("MainWindow", "영상타입"))
        self.push_button1.setText(_translate("MainWindow","Start"))
        self.push_button2.setText(_translate("MainWindow", "Quit"))

        self.comboBox.addItems(["1.5","2.0","2.5","3.0"])
        self.comboBox.setCurrentIndex(self.comboBox.findText("2.0",QtCore.Qt.MatchFixedString))

        self.comboBox_2.addItems(["10", "15", "20", "25"])
        self.comboBox_2.setCurrentIndex(self.comboBox_2.findText("15", QtCore.Qt.MatchFixedString))

        self.comboBox_4.addItems(["20", "25", "30", "35", "40", "45", "50"])
        self.comboBox_4.setCurrentIndex(self.comboBox_4.findText("35", QtCore.Qt.MatchFixedString))

        self.comboBox_3.addItems(["0.35", "0.40", "0.45", "0.50", "0.55", "0.60"])
        self.comboBox_3.setCurrentIndex(self.comboBox_3.findText("0.60", QtCore.Qt.MatchFixedString))

    def fileDialog(self):
        fileName = QFileDialog.getOpenFileName(None)
        return fileName[0]

    def updateUI(self,prog1,prog2,limit):
        value = prog2 / limit * 100
        if (value > 100):
            self.progressBar.setValue(100)
        else:
            self.progressBar.setValue(value)

        self.progressBar_2.setValue(prog1)
        
    def id_editFunc(self):
        self.lbl_textHere.setText(self.id_edit.text())

    def input_id(self):
        self.id = self.id_edit.text()


class Login(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("login.ui", self)
        self.setMinimumSize(294, 461)
        self.setMaximumSize(294, 461)
        self.inicio.clicked.connect(self.login)

    #########Connection Mysql###########
    def connecting(self):
        try:
            self.cursor = conn.cursor()
#             self.mysqlcursor = self.mydb.cursor()
        except pymysql.connector.errors.ProgrammingError as error:
            print("Review the Error -->", error)
            
    def test(self):
        QMessageBox.about(self, "message", "clicked")

    def login(self):
        self.connecting()
        user_name = self.usuario.text()
        password = self.contrasena.text()
        if user_name == "" and password == "":
            QMessageBox.warning(self, "Login", "Fill in the data", QMessageBox.Ok)
            self.destroy()
            
        else:
            get_data = (user_name, password)
            query = "SELECT * FROM user_info WHERE user_id = %s and user_password = %s"
            self.cursor.execute(query, get_data)
            validate = self.cursor.fetchall()
            if validate:
                QMessageBox.question(self, 'Login Successful', 'Correct username and password', QMessageBox.Ok)
                self.destroy()
                
                
            else:
                QMessageBox.warning(self, "Login Incorrect", "Incorrect user or password", QMessageBox.Ok)
                
