from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtCore import QRect, Qt
from watch import Watch
from PyQt6.QtGui import QFont, QFontDatabase

import sqlite3

class MainWindow(QMainWindow):
    def __init__(self, width, height, tab):
        super().__init__()

        self.width = width
        self.height = height
        self.tab = tab

        self.setGeometry(QRect(300, 200, width - 600, height  - 400))

        self.setStyleSheet("border-image: url(1.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        self.con = sqlite3.connect('main.db')
        self.cur = self.con.cursor()

        self.watch = QPushButton('START', self)
        self.exit = QPushButton('EXIT', self)

        id = QFontDatabase.addApplicationFont("LeticeaBumsteadCyrillic.otf")
        families = QFontDatabase.applicationFontFamilies(id)

        self.watch.setFont(QFont(families[0], 70))
        self.exit.setFont(QFont(families[0], 80))

        self.watch.resize(400, 250)
        self.exit.resize(400, 250)

        self.watch.setStyleSheet("QPushButton{border-image: url(2.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(3.png) 0 0 0 0  ;}")
        self.exit.setStyleSheet("QPushButton{border-image: url(2.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(3.png) 0 0 0 0  ;}")

        self.watch.move(750, 200)
        self.exit.move(750, 550)

        #self.watch.resize(320, 75)
        #self.exit.resize(320, 75)

        self.watch.clicked.connect(self.watch_func)
        self.exit.clicked.connect(self.exitfunc)

    def watch_func(self):
        self.tab.addTab(Watch(self.width, self.height, self), 'Показать')
        self.tab.setCurrentIndex(self.tab.count() - 1)

    def exitfunc(self):
        self.deleteLater()
