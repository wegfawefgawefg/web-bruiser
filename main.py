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
import requests
import re

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class WebBruiser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setGeometry(0, 0, 600, 800)
        self.setWindowTitle('Web Bruiser')
        self.visited_urls = []
        self.forward_back_cursor = 0

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

    def go(self, was_a_back_or_forward=False):
        # set status bar to "loading {url}"
        self.status_bar.setText("loading " + self.url_bar.text())
        url = self.url_bar.text()

        try:
            url = self.url_bar.text()
            url = self.format_raw_url(url)
            r = requests.get(url)
            if r.status_code != 200:
                self.error_invalid_url()
                return
            elif r.status_code == 200:
                if not was_a_back_or_forward:
                    print("not a back or forward")
                    # if the cursor is not at the end, then we need to remove the urls that are after the cursor
                    if self.forward_back_cursor != len(self.visited_urls) - 1:
                        self.visited_urls = self.visited_urls[:self.forward_back_cursor + 1]

                    self.visited_urls.append(url)
                    self.forward_back_cursor = len(self.visited_urls) - 1
                response_time = r.elapsed.total_seconds()
                self.status_bar.setText(f"loaded {self.url_bar.text()} in {response_time} seconds" )

                # # parse the html
                # html = r.text
                # # find all the links
                # links = re.findall(r'href=[\'"]?([^\'" >]+)', html)
                # # find all the images
                # images = re.findall(r'src=[\'"]?([^\'" >]+)', html)

                # # display the links
                # for link in links:
                #     self.text.append(link)
                # # display the images
                # for image in images:
                #     self.text.append(image)

                self.text.setText(r.text)
                # drop the text into a text file
                # with open("test.html", "w") as f:
                #     f.write(r.text)

        except Exception as e:
            print(e)
            self.error_invalid_url()
        
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
        if e.key() == Qt.Key_R:
            self.go()
        # back button on mouse
        if e.key() == Qt.Key_B:
            self.back()
        if e.key() == Qt.Key_H:
            self.history()

    def history(self):
        print(self.visited_urls)

    def back(self):
        if len(self.visited_urls) >= 2:
            self.url_bar.setText(self.visited_urls[self.forward_back_cursor - 1])
            # self.visited_urls.pop()
            self.go(was_a_back_or_forward=True)
            self.forward_back_cursor -= 1

    # maybe a forward button?

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