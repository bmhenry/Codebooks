from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from codebook_ui.settings_ui import *


"""Contains the UI for the main Codebooks window"""


class CodebooksMainUi(QtWidgets.QMainWindow):
    """Class containing the UI for the main Codebooks window"""
    def __init__(self, parent = None):
        super().__init__(parent)

        # set up the interface
        self.setupUi()

        # alert the ui that initialization is over
        self.startupCalled()

        # show the window
        self.show()


    def setupUi(self, parent = None):
        """Sets up the UI"""

        self.settingsWindow = None

        # Main window and widget setup
        self.setObjectName("MainWindow")
        #self.resize(990, 694)
        self.setFixedSize(990, 694)  # not resizable, for now

        # create central widget
        self.centralwidget = QtWidgets.QWidget()


        # set large label font
        labelFont = QtGui.QFont()
        labelFont.setPointSize(12)

        # Codebook files setup
        self.codebookLabel = QtWidgets.QLabel(self.centralwidget)
        self.codebookLabel.setGeometry(QtCore.QRect(16, 20, 91, 21))
        self.codebookLabel.setFont(labelFont)
        self.codebookLabel.setObjectName("codebookLabel")

        self.codebookTabs = QtWidgets.QTabWidget(self.centralwidget)
        self.codebookTabs.setGeometry(QtCore.QRect(16, 60, 191, 561))
        self.codebookTabs.setObjectName("codebookTabs")
        self.codebookTabs.currentChanged.connect(self.codebookTabChanged)

        # This part should probably be generated and not in here already
        # self.Cookbook1 = QtWidgets.QWidget()
        # self.Cookbook1.setObjectName("Cookbook1")
        # self.Cookbook1FileList = QtWidgets.QListView(self.Cookbook1)
        # self.Cookbook1FileList.setGeometry(QtCore.QRect(0, 0, 191, 561))
        # self.Cookbook1FileList.setFrameShadow(QtWidgets.QFrame.Plain)
        # self.Cookbook1FileList.setObjectName("Cookbook1FileList")

        # add in Codebook 1 after creating it
        #self.codebookTabs.addTab(self.Cookbook1, "")

        # File/Entry name
        self.entryName = QtWidgets.QLineEdit(self.centralwidget)
        self.entryName.setGeometry(QtCore.QRect(220, 20, 140, 21))
        self.entryName.setFont(labelFont)
        self.entryName.setObjectName("entryName")
        self.entryName.textEdited.connect(self.entryNameChanged)

        # Aesthetic vertical divider
        self.tagspacer = QtWidgets.QFrame(self.centralwidget)
        self.tagspacer.setGeometry(QtCore.QRect(380, 10, 20, 41))
        self.tagspacer.setFrameShape(QtWidgets.QFrame.VLine)
        self.tagspacer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tagspacer.setObjectName("tagspacer")

        # Tags bar label setup
        self.searchLabel = QtWidgets.QLabel(self.centralwidget)
        self.searchLabel.setGeometry(QtCore.QRect(410, 19, 80, 20))
        self.searchLabel.setObjectName("searchLabel")

        # Search bar setup
        self.searchBox = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBox.setGeometry(QtCore.QRect(490, 20, 440, 20))
        self.searchBox.setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.searchBox.setObjectName("searchBox")
        self.searchBox.textEdited.connect(self.searchbarChanged)

        # Tabs for Entry view
        self.entryTabs = QtWidgets.QTabWidget(self.centralwidget)
        self.entryTabs.setGeometry(QtCore.QRect(220, 60, 741, 561))
        self.entryTabs.setObjectName("entryTabs")

        # Label to communicate saved status
        self.savedStatus = QtWidgets.QLabel(self.centralwidget)
        self.savedStatus.setGeometry(QtCore.QRect(240,631, 80, 21))
        self.savedStatus.setObjectName("savedStatus")


        # put the central widget in the main window
        self.setCentralWidget(self.centralwidget)

        # set the menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 990, 21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuCode = QtWidgets.QMenu(self.menubar)
        self.menuCode.setObjectName("menuCode")

        self.menuCodebooks = QtWidgets.QMenu(self.menubar)
        self.menuCodebooks.setObjectName("menuCodebooks")

        # add settings option to menu bar
        self.actionSettings = QtWidgets.QAction(self)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.triggered.connect(self.openSettings)
        self.actionSettings.setText("Settings")

        # add menus to menu bar
        self.setMenuBar(self.menubar)
        

        # set the status bar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # MENU: File options    
        self.actionNew_File = QtWidgets.QAction(self)
        self.actionNew_File.setObjectName("actionNew_File")
        self.actionNew_File.triggered.connect(self.newFile)
        self.actionNew_File.setShortcut(QtGui.QKeySequence("Ctrl+Shift+N"))

        self.actionOpen_File = QtWidgets.QAction(self)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionOpen_File.triggered.connect(self.openFile)

        # self.actionSave_File = QtWidgets.QAction(self)
        # self.actionSave_File.setObjectName("actionSave_File")
        # self.actionSave_File.triggered.connect(self.saveFile)
        

        # self.actionSave_File_As = QtWidgets.QAction(self)
        # self.actionSave_File_As.setObjectName("actionSave_File_As")
        # self.actionSave_File_As.triggered.connect(self.saveFileAs)


        # Keep this one around for sure, just in case
        # self.actionClose_File = QtWidgets.QAction(self)
        # self.actionClose_File.setObjectName("actionClose_File")
        # self.actionClose_File.triggered.connect(self.closeFile)

        self.actionDelete_File = QtWidgets.QAction(self)
        self.actionDelete_File.setObjectName("actionDelete_File")
        self.actionDelete_File.triggered.connect(self.deleteFile)


        # MENU: entry options
        self.actionNew_Entry = QtWidgets.QAction(self)
        self.actionNew_Entry.setObjectName("actionNew_Entry")
        self.actionNew_Entry.triggered.connect(self.newEntry)
        self.actionNew_Entry.setShortcut(QtGui.QKeySequence("Ctrl+N"))

        self.actionImport_Entry = QtWidgets.QAction(self)
        self.actionImport_Entry.setObjectName("actionImport_Entry")
        self.actionImport_Entry.triggered.connect(self.importEntry)
        self.actionImport_Entry.setShortcut(QtGui.QKeySequence("Ctrl+O"))

        self.actionSave_Entry = QtWidgets.QAction(self)
        self.actionSave_Entry.setObjectName("actionSave_Entry")
        self.actionSave_Entry.triggered.connect(self.saveEntry)
        self.actionSave_Entry.setShortcut(QtGui.QKeySequence("Ctrl+S"))

        self.actionSave_Entry_As = QtWidgets.QAction(self)
        self.actionSave_Entry_As.setObjectName("actionSave_Entry_As")
        self.actionSave_Entry_As.setShortcut(QtGui.QKeySequence("Ctrl+Shift+S"))

        self.actionClose_Entry = QtWidgets.QAction(self)
        self.actionClose_Entry.setObjectName("actionClose_Entry")
        self.actionClose_Entry.triggered.connect(self.closeEntry)
        self.actionClose_Entry.setShortcut(QtGui.QKeySequence("Ctrl+W"))

        self.actionDelete_Entry = QtWidgets.QAction(self)
        self.actionDelete_Entry.setObjectName("actionDelete_Entry")
        self.actionDelete_Entry.triggered.connect(self.deleteEntry)


        # MENU: codebook options
        self.actionNew_Codebook = QtWidgets.QAction(self)
        self.actionNew_Codebook.setObjectName("actionNew_Codebook")
        self.actionNew_Codebook.triggered.connect(self.newCodebook)

        self.actionOpen_Codebook = QtWidgets.QAction(self)
        self.actionOpen_Codebook.setObjectName("actionOpen_Codebook")
        self.actionOpen_Codebook.triggered.connect(self.openCodebook)

        self.actionClose_Codebook = QtWidgets.QAction(self)
        self.actionClose_Codebook.setObjectName("actionClose_Codebook")
        self.actionClose_Codebook.triggered.connect(self.closeCodebook)

        self.actionDelete_Codebook = QtWidgets.QAction(self)
        self.actionDelete_Codebook.setObjectName("actionDelete_Codebook")
        self.actionDelete_Codebook.triggered.connect(self.deleteCodebook)

        self.actionInfo_Codebook = QtWidgets.QAction(self)
        self.actionInfo_Codebook.setObjectName("actionInfo_Codebook")
        self.actionInfo_Codebook.triggered.connect(self.codebookInfo)


        # add actions to menu
        self.menuFile.addAction(self.actionNew_File)
        self.menuFile.addAction(self.actionOpen_File)
        #self.menuFile.addAction(self.actionSave_File)
        #self.menuFile.addAction(self.actionSave_File_As)
        #self.menuFile.addAction(self.actionClose_File)
        self.menuFile.addAction(self.actionDelete_File)
        
        self.menuCode.addAction(self.actionNew_Entry)
        self.menuCode.addAction(self.actionImport_Entry)
        self.menuCode.addAction(self.actionSave_Entry)
        self.menuCode.addAction(self.actionSave_Entry_As)
        self.menuCode.addAction(self.actionClose_Entry)
        self.menuCode.addAction(self.actionDelete_Entry)

        self.menuCodebooks.addAction(self.actionNew_Codebook)
        self.menuCodebooks.addAction(self.actionOpen_Codebook)
        self.menuCodebooks.addAction(self.actionClose_Codebook)
        self.menuCodebooks.addAction(self.actionDelete_Codebook)
        self.menuCodebooks.addAction(self.actionInfo_Codebook)

        # add main menu actions to menu bar
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCodebooks.menuAction())
        self.menubar.addAction(self.menuCode.menuAction())
        self.menubar.addAction(self.actionSettings)


        # Button to get code
        self.getCodeButton = QtWidgets.QPushButton(self.centralwidget)
        self.getCodeButton.setGeometry(QtCore.QRect(854, 630, 91, 23))
        self.getCodeButton.setObjectName("getCodeButton")
        self.getCodeButton.clicked.connect(self.getCode)

        # finalize window
        # set automatic indexing for tabbed views
        self.codebookTabs.setCurrentIndex(0)
        self.entryTabs.setCurrentIndex(0)        

        # set names
        self.retranslateUi(self)

        QtCore.QMetaObject.connectSlotsByName(self)
        pass


    def retranslateUi(self, parent):
        """Renames UI elements and changes text where needed"""

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "CodeBook"))
        self.searchLabel.setText(_translate("MainWindow", "Search entries:"))
        self.codebookLabel.setText(_translate("MainWindow", "Codebooks:"))
        self.entryName.setPlaceholderText(_translate("MainWindow", "No Entry Selected"))
        self.searchBox.setPlaceholderText(_translate("MainWindow", "<separate tags with commas>"))
        self.savedStatus.setText(_translate("MainWindow", " "))
        self.getCodeButton.setText(_translate("MainWindow", "Get Code..."))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuCode.setTitle(_translate("MainWindow", "Code"))
        self.menuCodebooks.setTitle(_translate("MainWindow", "Codebooks"))
        self.actionNew_File.setText(_translate("MainWindow", "New File"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))
        #self.actionSave_File.setText(_translate("MainWindow", "Save File"))
        #self.actionSave_File_As.setText(_translate("MainWindow", "Save File As..."))
        #self.actionClose_File.setText(_translate("MainWindow", "Close File"))
        self.actionDelete_File.setText(_translate("MainWindow", "Delete File"))
        self.actionNew_Entry.setText(_translate("MainWindow", "New Entry"))
        self.actionImport_Entry.setText(_translate("MainWindow", "Import Entry..."))
        self.actionSave_Entry.setText(_translate("MainWindow", "Save Entry"))
        self.actionSave_Entry_As.setText(_translate("MainWindow", "Save Entry As..."))
        self.actionClose_Entry.setText(_translate("MainWindow", "Close Entry"))
        self.actionDelete_Entry.setText(_translate("MainWindow", "Delete Entry"))
        self.actionNew_Codebook.setText(_translate("MainWindow", "New Codebook"))
        self.actionOpen_Codebook.setText(_translate("MainWindow", "Open Codebook"))
        self.actionClose_Codebook.setText(_translate("MainWindow", "Close Codebook"))
        self.actionDelete_Codebook.setText(_translate("MainWindow", "Delete Codebook..."))
        self.actionInfo_Codebook.setText(_translate("MainWindow", "Codebook Details..."))

        pass


    # DEFAULT FUNCTIONS:
    # Override these to perform functions when actions happen

    def startupCalled(self):
        print("Not implemented")

    def importEntry(self):
        print("Not implemented")

    def saveEntryAs(self):
        print("Not implemented")

    def getCode(self):
        print("Not implemented")