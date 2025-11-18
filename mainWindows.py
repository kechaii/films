from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import QRect, Qt
from watch import Watch
from PyQt6.QtGui import QFont, QFontDatabase

import sqlite3


class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.setGeometry(QRect(300, 200, width - 600, height - 400))

        self.setStyleSheet("border-image: url(1.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.con = sqlite3.connect('main.db')
        self.cur = self.con.cursor()

        self.watch = QPushButton('START', self)
        self.exit = QPushButton('EXIT', self)

        id = QFontDatabase.addApplicationFont("LeticeaBumsteadCyrillic.otf")
        self.families = QFontDatabase.applicationFontFamilies(id)

        self.watch.setFont(QFont(self.families[0], 70))
        self.exit.setFont(QFont(self.families[0], 70))

        self.watch.resize(400, 250)
        self.exit.resize(400, 250)

        self.watch.setStyleSheet("QPushButton{border-image: url(2.png) 0 0 0 0  ; color: #ff384d;}"
                                 "QPushButton:hover{border-image: url(3.png) 0 0 0 0  ;}")
        self.exit.setStyleSheet("QPushButton{border-image: url(2.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(3.png) 0 0 0 0  ;}")

        self.watch.move(750, 200)
        self.exit.move(750, 550)

        # self.watch.resize(320, 75)
        # self.exit.resize(320, 75)

        self.watch.clicked.connect(self.watch_func)
        self.exit.clicked.connect(self.exitfunc)

        self.c = Watch(self.width, self.height, self)

    def watch_func(self):
        self.c.show()

    def exitfunc(self):
        self.deleteLater()
