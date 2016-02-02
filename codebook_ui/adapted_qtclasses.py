# some classes to expand on pyqt classes
from PyQt5 import QtWidgets, QtGui

class CBfilewidget(QtWidgets.QWidget):
    def __init__(self, parent = None, *, directory = None, subfolder = None):
        super().__init__(parent)
        self.entryName = None
        self.entryTags = None
        self.subfolder = subfolder
        self.directory = directory
        

class CBlistEntryItem(QtWidgets.QWidget):
    def __init__(self, parent = None, *, name = '', tagString = ''):
        super().__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.entryName = QtWidgets.QLabel(name)
        self.entryName.setObjectName("entryName")

        self.entryTags = QtWidgets.QLabel(tagString)
        self.entryTags.setObjectName("entryTags")

        self.verticalLayout.addWidget(self.entryName)
        self.verticalLayout.addWidget(self.entryTags)
        self.setLayout(self.verticalLayout)

        self.entryTags.setStyleSheet('color: rgb(145,145,145)')


    def setName(self, name):
        self.entryName.setText(name)


    def setTags(self, tagString):
        self.entryTags.setText(tagString)
        

class HelpWindow(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()
        self.setupUi(self.window)

    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(400,300)
        HelpWindow.setWindowTitle("Settings")

        self.centralwidget = QtWidgets.QWidget(HelpWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.testLabel = QtWidgets.QLabel("Pending suggestions.", self.centralwidget)
        self.testLabel.setGeometry(10,10,50,15)

        # end
        HelpWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

        pass