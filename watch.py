from PyQt6.QtWidgets import QPushButton, QLineEdit, QMainWindow, QWidget, QCheckBox, QListWidget, QLabel, QRadioButton
from PyQt6.QtCore import QRect, Qt, QThread, pyqtSignal
from consts import FILTER_TYPE, SORTED_TYPE, GENRES, DICT_FILTER, DICT_GENRES, DICT_FILTER_NUM, DICT_GENRES_NUM
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap
from film import Film


class FactorialThread(QThread):
    result_ready = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        result = 1
        for i in range(1, 100000):
            result *= i
        self.result_ready.emit(result)


class Watch(QMainWindow):
    def __init__(self, width, height, widget):
        super(Watch, self).__init__(widget)

        self.setGeometry(QRect(300, 200, width - 600, height - 400))
        self.setStyleSheet("border-image: url(6.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.cur = widget.cur
        self.width = width
        self.height = height
        self.widget = widget

        step = (width - 600 - 225 * 2) - 235 * 5
        start = 0

        id = QFontDatabase.addApplicationFont("Montserrat-Medium.ttf")
        self.families = QFontDatabase.applicationFontFamilies(id)
        print(-1)

        self.widget_list = QListWidget(self)
        self.widget_list.move(195, 150)
        self.widget_list.resize(width - 600 - 195 * 2, 800)
        self.widget_list.setStyleSheet("border-image: url(0.png) 0 0 0 0;")
        print(0)

        self.back = QPushButton('', self)
        self.back.resize(81, 81)
        self.back.move(10, 10)
        self.back.clicked.connect(self.exit)
        self.back.setStyleSheet("QPushButton{border-image: url(13.png) 0 0 0 0;  color: #000000;}"
                                "QPushButton:hover{border-image: url(14.png) 0 0 0 0  ;}")
        print(1)

        self.add = QPushButton('', self)
        self.add.resize(81, 81)
        self.add.move(499, 10)
        self.add.clicked.connect(self.add_func)
        self.add.setStyleSheet("QPushButton{border-image: url(15.png) 0 0 0 0;  color: #000000;}"
                               "QPushButton:hover{border-image: url(16.png) 0 0 0 0  ;}")
        print(2)

        self.x = [start, start + step, start + step * 2, start + step * 3, start + step * 4]

        self.types = FILTER_TYPE[:]
        self.genres = GENRES[:]
        self.sortedFilm = SORTED_TYPE[0]
        print(3)

        self.all_films = list(self.cur.execute(f'''SELECT id, title, info, type, genre, estimation FROM films'''))
        self.all_films = [list(i) for i in self.all_films]
        print(4)

        # self.thread = FactorialThread(self.all_films)
        # self.thread.result_ready.connect(self.create_buttons_films)
        # self.thread.start()

        self.create_buttons_films()
        print(5)
        self.search = QLineEdit(self)
        # self.search.textChanged.connect(self.reset_list)
        self.search.editingFinished.connect(self.reset_list)

        self.search.setFont(QFont(widget.families[0], 30))

        self.search.resize(530, 81)
        self.search.move(600, 10)
        self.search.setTextMargins(30, 0, 80, 0)
        self.search.setStyleSheet("QLineEdit{border-image: url(9.png) 0 0 0 0;  color: #000000;}"
                                  "QLineEdit:hover{border-image: url(10.png) 0 0 0 0  ;}")
        print(6)

        self.reset_list()
        print(7)

        self.button_filter = QCheckBox('', self)
        self.button_filter.move(1150, 10)
        self.button_filter.resize(81, 81)
        self.button_filter.clicked.connect(self.show_filter)
        self.button_filter.setStyleSheet("QCheckBox{border-image: url(0.png) 0 0 0 0  ; }"
                                         "QCheckBox::indicator:unchecked {image: url(171.png) 0 0 0 0;}"
                                         "QCheckBox::indicator:unchecked:hover {image: url(181.png) 0 0 0 0;}"
                                         "QCheckBox::indicator:checked{image: url(181.png) 0 0 0 0  ;}"
                                         "QCheckBox::indicator:checked:hover{image: url(181.png) 0 0 0 0  ;}")

        self.button_sorted = QCheckBox('', self)
        self.button_sorted.move(1251, 10)
        self.button_sorted.resize(81, 81)
        self.button_sorted.clicked.connect(self.show_sorted)
        self.button_sorted.setStyleSheet("QCheckBox{border-image: url(0.png) 0 0 0 0  ; }"
                                         "QCheckBox::indicator:unchecked {image: url(111.png) 0 0 0 0;}"
                                         "QCheckBox::indicator:unchecked:hover {image: url(121.png) 0 0 0 0;}"
                                         "QCheckBox::indicator:checked{image: url(121.png) 0 0 0 0  ;}"
                                         "QCheckBox::indicator:checked:hover{image: url(121.png) 0 0 0 0  ;}")
        print(8)

        self.create_widget()
        print(9)

        self.c = Film(self.width, self.height, self)
        print(10)

    def create_buttons_films(self):
        for en, i in enumerate(self.all_films):
            button = QPushButton(str(i[0]), self.widget_list)
            button.resize(235, 349)
            button.clicked.connect(self.check_film)
            button.setStyleSheet("QPushButton{border-image: url(f.png) 0 0 0 0  ; color: transparent;}"
                                 "QPushButton:hover{border-image: url(fh.png) 0 0 0 0  ;}")

            label = QLabel(i[1], button)
            label.resize(190, 50)
            label.move(30, 210)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            label.setFont(QFont(self.widget.families[0], 15))
            label.setStyleSheet('color: #FFFFFF; ')

            genre = QLabel(f"Genre: {DICT_GENRES_NUM[i[4]]}", button)
            genre.resize(190, 18)
            genre.move(24, 271)
            genre.setFont(QFont(self.families[0], 10))
            genre.setStyleSheet('color: #FFFFFF;')

            types = QLabel(f"Type: {DICT_FILTER_NUM[i[3]]}", button)
            types.resize(190, 18)
            types.move(24, 290)
            types.setFont(QFont(self.families[0], 10))
            types.setStyleSheet('color: #FFFFFF;')

            estimation = QLabel(f"Rating: {i[5] / 10}", button)
            estimation.resize(190, 18)
            estimation.move(24, 310)
            estimation.setFont(QFont(self.families[0], 10))
            estimation.setStyleSheet('color: #FFFFFF;')

            button.show()

            self.all_films[en].append(button)

    def add_func(self):
        self.c.id_film = 0
        self.c.set_info()
        self.c.show()

    def check_film(self):
        self.c.id_film = int(self.sender().text())
        self.c.set_info()
        self.c.show()

    def show_sorted(self):
        if self.button_sorted.isChecked():
            self.widget_sorted.show()
            if self.button_filter.isChecked():
                self.button_filter.click()
        else:
            self.widget_sorted.hide()

    def show_filter(self):
        if self.button_filter.isChecked():
            self.widget_filter.show()
            if self.button_sorted.isChecked():
                self.button_sorted.click()
        else:
            self.widget_filter.hide()

    def create_widget(self):
        self.widget_filter = QWidget(self)
        self.widget_sorted = QWidget(self)

        self.widget_sorted.hide()
        self.widget_filter.hide()
        self.widget_sorted.resize(200, 50 * len(SORTED_TYPE))
        self.widget_filter.resize(200, 50 * (len(FILTER_TYPE) + len(GENRES)))

        self.widget_sorted.setStyleSheet("QWidget{border-image: url(fon.png) 0 0 0 0  ; }")
        self.widget_filter.setStyleSheet("QWidget{border-image: url(fon.png) 0 0 0 0  ; }")

        self.widget_sorted.move(self.button_sorted.x() - 50, self.button_sorted.y() + 85)
        self.widget_filter.move(self.button_filter.x() - 50, self.button_filter.y() + 85)

        y = 20
        for i in self.types:
            checkbox = QCheckBox(DICT_FILTER_NUM[i], self.widget_filter)
            checkbox.move(20, y)
            checkbox.setStyleSheet("QCheckBox{border-image: url(0.png) 0 0 0 0  ; }"
                                   "QCheckBox::indicator:unchecked {image: url(coff.png);}"
                                   "QCheckBox::indicator:unchecked:hover {image: url(coffh.png);}"
                                   "QCheckBox::indicator:checked{image: url(con.png);}"
                                   "QCheckBox::indicator:checked:hover{image: url(conh.png);}")
            checkbox.setFont(QFont(self.widget.families[0], 20))
            checkbox.click()
            checkbox.clicked.connect(self.set_filter)
            y += 35
        for i in self.genres:
            checkbox = QCheckBox(DICT_GENRES_NUM[i], self.widget_filter)
            checkbox.move(20, y)
            checkbox.setStyleSheet("QCheckBox{border-image: url(0.png) 0 0 0 0  ; }"
                                   "QCheckBox::indicator:unchecked {image: url(coff.png);}"
                                   "QCheckBox::indicator:unchecked:hover {image: url(coffh.png);}"
                                   "QCheckBox::indicator:checked{image: url(con.png); }"
                                   "QCheckBox::indicator:checked:hover{image: url(conh.png);}")
            checkbox.setFont(QFont(self.widget.families[0], 20))
            checkbox.click()
            checkbox.clicked.connect(self.set_filter)
            y += 35
        y = 20
        for i in SORTED_TYPE:
            radiobutton = QRadioButton(i, self.widget_sorted)
            radiobutton.move(20, y)
            radiobutton.setStyleSheet("QRadioButton{border-image: url(0.png) 0 0 0 0  ; }"
                                      "QRadioButton::indicator:unchecked {image: url(roff.png); }"
                                      "QRadioButton::indicator:unchecked:hover {image: url(roffh.png);}"
                                      "QRadioButton::indicator:checked{image: url(ron.png);}"
                                      "QRadioButton::indicator:checked:hover{image: url(ronh.png);}")
            radiobutton.setFont(QFont(self.widget.families[0], 20))
            if i == SORTED_TYPE[0]:
                radiobutton.click()
            radiobutton.clicked.connect(self.set_sorted)

            y += 35

    def set_sorted(self):
        self.sortedFilm = self.sender().text()
        self.reset_list()

    def set_filter(self):
        title = self.sender().text()

        if self.sender().isChecked():
            if title in DICT_GENRES:
                self.genres.append(DICT_GENRES[title])
            else:
                self.types.append(DICT_FILTER[title])
        else:
            if title in DICT_GENRES:
                self.genres.remove(DICT_GENRES[title])
            else:
                self.types.remove(DICT_FILTER[title])
        self.reset_list()

    def reset_list(self):
        if self.sortedFilm == 'Алфавит':
            self.all_films = sorted(self.all_films, key=lambda x: x[1])

        elif self.sortedFilm == 'Рейтинг':
            self.all_films = sorted(self.all_films, key=lambda x: x[5])[::-1]

        y = en = 0
        text = self.search.text().lower()

        for i in self.all_films:
            flag = 1

            if (en + 1) % 6 == 0:
                y += 400

            if i[4] not in self.genres:
                flag = 0
            if i[3] not in self.types:
                flag = 0

            if text != '':
                if text not in i[1].lower():
                    flag = 0

            if flag:
                i[-1].show()
                i[-1].move(self.x[en % 5], y)
                en += 1
            else:
                i[-1].hide()

    def exit(self):
        self.hide()
