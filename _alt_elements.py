from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QTextOption
from PyQt5 import Qt

class CodebooksTextBox(QPlainTextEdit):
    def CodebooksTextBox(self):
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        pass
    
    def keyPressEvent(self,  event):
        if event == Qt.Key_Return or event == Qt.Key_Enter:
            pass
        else:
            QPlainTextEdit.keyPressEvent(event)