import cv2
import numpy as np
import dlib
import imutils
from imutils import face_utils
from imutils.video import FPS
from scipy.spatial import distance
import condition1
import condition2
import sys
from UI import *
import time
import pymysql
import pygame
from timeit import default_timer as timer
from datetime import timedelta, datetime
import datetime

condition1_Value = 0.0
condition2_Value = 0.0
fpsValue = 0.1e-5
drowsiness = 0.6
DOWNSAMPLE_RATIO = 1
SKIP_FRAMES = 1
count = 0
count_DB = 0
currentRect = [0,0,0,0]
frameCount = 0
hogFaceDetector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
conn = pymysql.connect(host='localhost',
                           user='pi',
                           password='raspberry',
                           db='suppoter',
                           charset='utf8')
pygame.init()



class ShowVideo(QtCore.QObject):
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    t_UI = QtCore.pyqtSignal()
    cap = cv2.VideoCapture(0)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)
       

    @QtCore.pyqtSlot()
    def startVideo(self):
        global frame
        global gray
        global fpsValue
        global DOWNSAMPLE_RATIO
        global SKIP_FRAMES
        global count
        global currentRect
        global frame_counter
        global userID
        global start
        global end
        
        fps = FPS().start()
        ui.image_viewer1.show()
        start = timer() # 타이머 시작 변수
        while True:

            ret, frame = self.cap.read()
            LoopVideo(self.cap,True)

            if(ret==False):
                print("영상을 불러올 수 없습니다.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 2.GrayScaling
            if (DOWNSAMPLE_RATIO != 1.0):
                gray = cv2.resize(gray, (0, 0), fx=1 / DOWNSAMPLE_RATIO, fy=1 / DOWNSAMPLE_RATIO, interpolation = cv2.INTER_LINEAR)

            count += 1
            if(count % SKIP_FRAMES == 0):
                faceRects = hogFaceDetector(gray, 0)

                if (len(faceRects) == 0):
                    print("Face Not Detected.")
                    checkCondition(None,1)
                    fps.update()
                    fps.stop()

                else:
                    fps.update()
                    fps.stop()
                    fpsValue = fps.fps()
                    drawRect(driverRect(faceRects))
                    drawEyes(driverRect(faceRects))
                    checkCondition(shape,0)
                    user_id = ui2.usuario.text() # id값
                    
                    end = timer() * 2
                    
                    study_time = timedelta(seconds=end - start)
                    today_date = datetime.datetime.today().strftime("%Y%m%d")
                    curs = conn.cursor()
                    sql = "update study_manager set study_time ='" + str(study_time) + "' where id='" + user_id + "' and study_date='" + today_date + "'"
                    curs.execute(sql)
                    conn.commit()

            else:
                drawFakeRect()

            frame = cv2.resize(frame, (600, 440))
            color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    int(600),
                                    int(440-4),
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)
            self.t_UI.emit()

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(10, loop.quit)
            loop.exec_()
            

def drawRect(faceRect):
    global DOWNSAMPLE_RATIO
    global currentRect
    x1 = int(faceRect.left()*DOWNSAMPLE_RATIO)
    y1 = int(faceRect.top()*DOWNSAMPLE_RATIO)
    x2 = int(faceRect.right()*DOWNSAMPLE_RATIO)
    y2 = int(faceRect.bottom()*DOWNSAMPLE_RATIO)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    currentRect = [x1,y1,x2,y2]

def drawFakeRect():
    global DOWNSAMPLE_RATIO
    global currentRect

    x1 = int(currentRect[0])
    y1 = int(currentRect[1])
    x2 = int(currentRect[2])
    y2 = int(currentRect[3])
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

def drawEyes(faceRect):
    global shape
    shape = predictor(gray, faceRect)
    shape = face_utils.shape_to_np(shape)
    for (x, y) in shape[36:48]:#37~48
        cv2.circle(frame, (int(x*DOWNSAMPLE_RATIO), int(y*DOWNSAMPLE_RATIO)), 1, (0, 0, 255), -1)

def calcEyeRatio(shape):
    H1 = distance.euclidean(shape[37], shape[41])#Top1 Bottom1
    H2 = distance.euclidean(shape[38], shape[40])#Top2 Bottom2
    W = distance.euclidean(shape[36], shape[39])#Left Right
    result = (H1 + H2) / (W)

    return result

def driverRect(faceRects):
    """여러 개의 얼굴이 인식될 시, 가장 큰 면적을 가진 사람을 운전자로 함"""
    biggestArea = 0

    if (len(faceRects) == 1):
        return faceRects[0]
    else:
        for faceRect in faceRects:
            x1 = faceRect.left()
            y1 = faceRect.top()
            x2 = faceRect.right()
            y2 = faceRect.bottom()
            area = (x2-x1) * (y2-y1)

            if (area>biggestArea):
                biggestArea = area
                driver = faceRect

        return driver

def updateDrowsniss(value):
    global drowsiness
    drowsiness = float(value)

def checkCondition(shape,flag):#flag = 1 => Not detection
    global condition1_Value
    global condition2_Value
    global drowsiness
    global count_DB
    global count

    Now = time.localtime()

    if(flag==1):
        condition2.q.put(False)
        condition1_Value = condition1.subValue(condition1_Value, fpsValue)
        condition2.controlQueueLen(fpsValue)
        condition2_Value = condition2.calcTrueRatio()
        return

    if (calcEyeRatio(shape) < drowsiness):
        condition2.q.put(True)
        condition1_Value = condition1.addValue(condition1_Value, fpsValue)
        #if(condition1.checkCondition(condition1_Value)==True):
    else:
        condition2.q.put(False)
        condition1_Value = condition1.subValue(condition1_Value, fpsValue)

    condition2.controlQueueLen(fpsValue)
    condition2_Value = condition2.calcTrueRatio()

    if (condition2.checkCondition(condition2_Value) == True):
        count+=1 #check
        #embeded_db.close()
        if((count-1)/2 >= 15):
            soundObj = pygame.mixer.Sound('alarm.wav')
            soundObj.play(0)

            print("alarm")
            count = 0


def setVideoPath(ui,vid):
    if ui.radio.isChecked():
        vid.cap = cv2.VideoCapture(0)

    if ui.radio_2.isChecked():
        path = ui.fileDialog()
        vid.cap = cv2.VideoCapture(path)

def LoopVideo(vid,bool):
    global frameCount

    if (bool):
        frameCount += 1
        if frameCount >= vid.get(cv2.CAP_PROP_FRAME_COUNT)-30:
            frameCount = 0
            vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)
    
    ui2 = Login()
    ui2.show()
    

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    vid.VideoSignal1.connect(ui.image_viewer1.setImage)

    vid.t_UI.connect(lambda: ui.updateUI(condition1_Value,condition2_Value, condition2.limit))
    ui.push_button1.clicked.connect(vid.startVideo)
    ui.push_button2.clicked.connect(QtCore.QCoreApplication.instance().quit)
    ui.comboBox.currentTextChanged.connect(lambda: condition1.updateTime(ui.comboBox.currentText()))
    ui.comboBox_2.currentTextChanged.connect(lambda: condition2.updateTime(ui.comboBox_2.currentText()))
    ui.comboBox_4.currentTextChanged.connect(lambda: condition2.updateLimit(ui.comboBox_4.currentText()))
    ui.comboBox_3.currentTextChanged.connect(lambda: updateDrowsniss(ui.comboBox_3.currentText()))
    ui.radio.clicked.connect(lambda: setVideoPath(ui,vid))
    ui.radio_2.clicked.connect(lambda: setVideoPath(ui,vid))

    MainWindow.show()
    sys.exit(app.exec_())
