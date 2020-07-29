# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pymysql
from PyQt5 import uic
from py_rc import passowrd_rc, user_rc, user_profile_rc, login_rc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
import signal


from UI import *
from Detector import *

embeded_db = pymysql.connect(
    user='root', 
    passwd='1234', 
    host='127.0.0.1', 
    db='mysql', 
    charset='utf8')


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
            self.cursor = embeded_db.cursor()
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
            
        else:
            get_data = (user_name, password)
            query = "SELECT * FROM embeded_test WHERE id = %s and passwd = %s;"
            self.cursor.execute(query, getdata)
            validate = self.cursor.fetchall()
            print(get_data)
            get_userID(user_name)
            if validate:
                QMessageBox.question(self, 'Login Successful', 'Correct username and password', QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Login Incorrect", "Incorrect user or password", QMessageBox.Ok)
                
    def get_userID(self,userID):
        return userId


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
