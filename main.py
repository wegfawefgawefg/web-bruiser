''' web-bruiser, a minimal web browser written entirely in python '''
'''
design docs:
need a url bar, 
need a refresh keypress,

need a way to display the html
need a way to display the images

need a way to display the links
clicking on a link should open the link in the same window

only one tab is fine, no need for multiple tabs

need a way to display the javascript???
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QTextEdit, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QVector2D
import requests
import re

class WebBruiser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setGeometry(0, 0, 600, 800)
        self.setWindowTitle('Web Bruiser')

        self.bar_height = 30

        self.url_bar = QLineEdit(self)
        self.url_bar.setStyleSheet("background-color: #333333; color: #aaaaaa;")
        self.url_bar.returnPressed.connect(self.go)

        self.status_bar = QTextEdit(self)
        self.status_bar.setReadOnly(True)

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setText("home page")

        self.resize_elements()

        self.show()

    def go(self):
        # set status bar to "loading {url}"
        self.status_bar.setText("loading " + self.url_bar.text())
        url = self.url_bar.text()

        try:
            url = self.url_bar.text()
            url = self.format_raw_url(url)
            r = requests.get(url)
            # if the url is invalid, set status bar to "invalid url"
            if r.status_code != 200:
                self.error_invalid_url()
                return
            elif r.status_code == 200:
                self.status_bar.setText("loaded " + self.url_bar.text())
                self.text.setText(r.text)
        except Exception as e:
            print(e)
            self.error_invalid_url()
        

    def clear_url_bar(self):
        is_default = self.url_bar.text().startswith("enter url")
        print("is default: ", is_default)
        if is_default:
            self.url_bar.setText(self.url_bar.text()[len("enter url"):])

    def error_invalid_url(self):
        url = self.url_bar.text()
        target_url = self.format_raw_url(url)
        self.status_bar.setText(f"invalid url {target_url}")

    def format_raw_url(self, url):
        if not url.startswith("http://"):
            url = "http://" + url
        return url


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q or e.key() == Qt.Key_Escape:
            self.close()
        # refresh on press r
        if e.key() == Qt.Key_R:
            self.refresh()

    def resize_elements(self):
        self.url_bar.resize(self.width(), self.bar_height)
        self.url_bar.move(0, 0)
        self.status_bar.resize(self.width(), self.bar_height)
        self.status_bar.move(0, self.height() - self.bar_height)
        self.text.resize(self.width(), self.height() - self.bar_height * 2)
        self.text.move(0, self.bar_height)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.resize_elements()




    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    webBruiser = WebBruiser()
    sys.exit(app.exec_())