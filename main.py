''' web-bruiser, a minimal web browser written entirely in python '''
'''
design docs:
need a url bar, 
need a back button,
need a forward button,
need a refresh button,

need a way to display the html
need a way to display the images

need a way to display the links
clicking on a link should open the link in the same window

only one tab is fine, no need for multiple tabs

need a way to display the javascript
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt

class WebBruiser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 600, 800)
        self.setWindowTitle('Web Bruiser')
        # add the url bar
        self.urlBar = QLineEdit(self)
        # add the back button
        self.backButton = QPushButton('<', self)
        # add the forward button
        self.forwardButton = QPushButton('>', self)
        # add a go button
        self.goButton = QPushButton('Go', self)

        # add the html display
        self.htmlDisplay = QTextEdit(self)

        self.show()

    #quit on press q
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()
        # refresh on press r
        if e.key() == Qt.Key_R:
            self.refresh()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    webBruiser = WebBruiser()
    sys.exit(app.exec_())