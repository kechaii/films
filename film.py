from PyQt6.QtWidgets import QPushButton, QLineEdit, QMainWindow, QWidget, QCheckBox, QListWidget, QLabel
from PyQt6.QtCore import QRect, Qt
from consts import FILTER_TYPE, SORTED_TYPE, GENRES
from PyQt6.QtGui import QFont


class Film(QMainWindow):
    def __init__(self, width, height, widget):
        super(Film, self).__init__(widget)

        self.setGeometry(QRect(300, 200, width - 600, height - 400))
        self.setStyleSheet("border-image: url(7.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.id_film = 0

        self.cur = widget.cur

        self.back = QPushButton('', self)
        self.back.resize(81, 81)
        self.back.move(10, 10)
        self.back.clicked.connect(self.exit)
        self.back.setStyleSheet("QPushButton{border-image: url(13.png) 0 0 0 0;  color: #000000;}"
                                "QPushButton:hover{border-image: url(14.png) 0 0 0 0  ;}")

        self.title_on_banner = QLabel('', self)

        self.title = QLineEdit(self)
        self.title.editingFinished.connect(self.reset_title)

        self.edit = QCheckBox('', self)
        self.edit.move(1150, 10)
        self.edit.resize(81, 81)
        self.edit.clicked.connect(self.switch_edit)
        self.edit.setStyleSheet("QCheckBox{border-image: url(0.png) 0 0 0 0  ; }"
            "QCheckBox::indicator:unchecked {image: url(21.png) 0 0 0 0;}"
                                "QCheckBox::indicator:unchecked:hover {image: url(22.png) 0 0 0 0;}"
                                "QCheckBox::indicator:checked{image: url(22.png) 0 0 0 0  ;}"
                                "QCheckBox::indicator:checked:hover{image: url(22.png) 0 0 0 0  ;}")


    def set_info(self):
        if self.id_film == 0:
            self.edit.hide()
            self.film = ['', '', 0, 0, 0]
        else:
            self.film = list(list(
                self.cur.execute(
                    f'''SELECT title, info, type, genre, estimation FROM films WHERE id == {self.id_film}'''))[
                                 0])

            self.title.setReadOnly(True)
            self.title.setText(self.film[0])
            self.title_on_banner.setText(self.film[0])
            self.edit.show()

    def switch_edit(self):
        if self.edit.isChecked():
            pass
        else:
            pass

    def reset_title(self):
        self.title_on_banner.setText(self.title.text())

    def exit(self):
        self.hide()
