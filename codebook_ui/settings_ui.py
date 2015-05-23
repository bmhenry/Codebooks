from PyQt5 import QtCore, QtGui, QtWidgets


class SettingsWindow(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()
        self.setupUi(self.window)
        self.window.show()

    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(400,300)
        SettingsWindow.setWindowTitle("Settings")

        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.testLabel = QtWidgets.QLabel("Pending suggestions.", self.centralwidget)
        self.testLabel.setGeometry(10,10,50,15)

        # end
        SettingsWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

        pass