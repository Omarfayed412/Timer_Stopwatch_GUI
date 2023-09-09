from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from StopWatch import Ui_TimerWin as stpwtchUI
from Timer import Ui_TimerWin as timerUI
from Main import Ui_MainWindow as MainUI

#sys will allow us to control the start and exit of the program  
import sys

class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #Main counters
        self.count_sec = 0
        self.count_min = 0
        self.count_hr = 0
        self.duration = 0

        self.flag = False
                
        self.ui = MainUI()
        self.ui.setupUi(self)

        #Setting up Stopwatch window
        self.winStp = QtWidgets.QMainWindow()
        self.uiStp = stpwtchUI()
        self.uiStp.setupUi(self.winStp)
        self.timer1 = QtCore.QTimer(self.winStp)

        #Setting up Timer window
        self.winTim = QtWidgets.QMainWindow()
        self.uiTim = timerUI()
        self.uiTim.setupUi(self.winTim)
        self.timer2 = QtCore.QTimer(self.winTim)
        
        #Assigning general signals to slots
        self.ui.Timer_btn.clicked.connect(self.open_winTim)
        self.ui.Stopp_btn.clicked.connect(self.open_WinStp)
        self.ui.exitMain.clicked.connect(self.close)


    #Routine of the Stop watch mode
    def stpOn(self):
        self.Reset()
        #creating actions 
        self.uiStp.Restart_btn.clicked.connect(self.Reset)
        self.uiStp.start_btn.clicked.connect(self.Start)
        self.uiStp.Stop_btn.clicked.connect(self.Stop)

        self.printTime()

        self.uiStp.exitStp.clicked.connect(self.close_winStp)

        #Create an object timer that can run parallel to the main code
        self.timer1.timeout.connect(self.get_time_Stp)

        #Fire a timeout signal each second
        self.timer1.start(1000)

    #Routine of the Timer mode
    def timOn(self):
        self.Reset()

        #creating actions 
        self.uiTim.Restart_btn.clicked.connect(self.Reset)
        self.uiTim.start_btn.clicked.connect(self.Start)
        self.uiTim.Stop_btn.clicked.connect(self.Stop)

        #Only update the counters if the timer is not working
        if self.flag == False:
            #Assigning the values in the spinboxes to the counters
            self.uiTim.Sec_box.valueChanged.connect(self.updateVal)
            self.uiTim.Min_box.valueChanged.connect(self.updateVal)
            self.uiTim.Hr_box.valueChanged.connect(self.updateVal)

        self.uiTim.exitTim.clicked.connect(self.close_winTim)

        self.timer2.timeout.connect(self.get_time_Tmr)
        self.timer2.start(1000)


    def Start(self):
        self.flag = True

    def Stop(self):
        self.flag = False

    def printTime(self):
        self.uiStp.Sec_lb.display(self.count_sec)
        self.uiStp.Min_lb.display(self.count_min)
        self.uiStp.Hr_lb.display(self.count_hr)

        self.uiTim.Sec_lb.display(self.count_sec)
        self.uiTim.Min_lb.display(self.count_min)
        self.uiTim.Hr_lb.display(self.count_hr)

    def Reset(self):
        self.flag = False
        self.count_hr = self.count_min = self.count_sec = 0
        self.printTime()

    # Method that updates the counters accordubg to value of the spinBox 
    def updateVal(self):
        self.count_sec = self.uiTim.Sec_box.value()
        self.count_min = self.uiTim.Min_box.value()
        self.count_hr = self.uiTim.Hr_box.value()

        #Whole duration measured in seconds to update progress bar
        self.duration = self.count_sec + (self.count_hr * 60 * 60) + (self.count_min * 60)
        self.uiTim.progressBar.setMaximum(self.duration)
                
    #Main function of the counters of Stop watch
    def get_time_Stp(self):
        if self.flag:
            self.count_sec += 1

            if self.count_sec < 60:
                self.printTime()
                    
            elif self.count_sec == 60:
                self.count_min += 1 
                self.count_sec = 0
                self.printTime()

            if self.count_min == 60:
                self.count_min = 0
                self.count_hr += 1
                self.printTime()

    def get_time_Tmr(self):
        if self.flag:
            #Update the progress bar
            self.uiTim.progressBar.setValue(self.duration)
            self.duration -= 1 

            if self.count_sec > 0:
                self.printTime()
                self.count_sec -= 1

            elif self.count_sec == 0 and self.count_min != 0:
                self.printTime()
                self.count_min -= 1 
                self.count_sec = 59 

            elif self.count_min == 0 and self.count_hr != 0:
                self.printTime()
                self.count_min = 59
                self.count_sec = 59
                self.count_hr -= 1

            elif self.count_hr == self.count_min == self.count_sec == 0:
                self.Reset() 

    def open_winTim(self):
        self.winTim.show()
        self.timOn()

    def open_WinStp(self):
        self.winStp.show()
        self.stpOn()

    def close_winTim(self):
        self.winTim.close()
        self.timer2.stop()
        

    def close_winStp(self):
        self.winStp.close()
        #Here im closing the object timer1 again to ensure there wont be any collisions between two modes
        self.timer1.stop()

# create app instance
app = QtWidgets.QApplication(sys.argv)
 
# create the instance of our Window
window = Mainwindow()

window.show()

# start the app and add it to the event loop
sys.exit(app.exec())


#Author: Omar Fayed
#Date: 9/8/2023