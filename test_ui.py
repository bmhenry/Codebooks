import sys
from PyQt5 import QtWidgets, QtCore, QtGui
#from _alt_elements import *

def startTest():
    print('Starting test...')

    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow()

    sys.exit(app.exec_())
    pass


class TestWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(TestWindow, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(300,300)

        self.label1 = QtWidgets.QLabel("hi", self)
        self.label1.setGeometry(QtCore.QRect(10,0,30,20))
        self.label1.setObjectName("label1")

        self.textbox = QtWidgets.QLineEdit(self) 
        self.textbox.setGeometry(QtCore.QRect(20,20,50,20))
        self.textbox.setObjectName("textbox")

        self.show()
        pass

    def closeEvent(self, event):
        print("Exiting...")
        super().closeEvent(event)
        pass

if __name__ == '__main__':
    startTest()