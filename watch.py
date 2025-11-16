from PyQt6.QtWidgets import QPushButton, QLineEdit, QMainWindow, QWidget, QCheckBox
from PyQt6.QtCore import QRect, Qt
from consts import FILTER_TYPE, SORTED_TYPE, GENRES

class Watch(QMainWindow):
    def __init__(self, width, height, widget):
        super().__init__()

        self.setGeometry(QRect(300, 200, width - 600, height  - 400))
        self.setStyleSheet("border-image: url(5.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.cur = widget.cur

        self.types = [i + 1 for i in range(len(FILTER_TYPE))]
        self.genres = [i + 1 for i in range(len(GENRES))]
        self.sortedFilm = SORTED_TYPE[0]

        self.film = list(self.cur.execute(f'''SELECT id, title, info, type, genre, estimation FROM films'''))

        self.reset = QPushButton('обновить', self)
        self.reset.clicked.connect(self.reset_list)

        self.search = QLineEdit(self)
        self.search.textChanged.connect(self.reset_list)
        #self.search.editingFinished.connect(self.reset_list)
        self.search.move(100, 100)

        self.show_list()
        self.reset_list()

        self.button_filter = QCheckBox('фильтр', self)
        self.button_filter.move(0, 400)
        self.button_filter.clicked.connect(self.show_filter)

        self.button_sorted = QCheckBox('сортировка', self)
        self.button_sorted.move(0, 500)
        self.button_sorted.clicked.connect(self.show_sorted)

        self.create_widget()

    def show_list(self):
        pass

    def show_sorted(self):
        if self.button_sorted.isChecked():
            self.widget_sorted.show()
        else:
            self.widget_sorted.hide()

    def show_filter(self):
        if self.button_filter.isChecked():
            self.widget_filter.show()
        else:
            self.widget_filter.hide()

    def create_widget(self):
        self.widget_filter = QWidget(self)
        self.widget_sorted = QWidget(self)

        self.widget_sorted.hide()
        self.widget_filter.hide()
        self.widget_sorted.resize(100, 30 * len(SORTED_TYPE))
        self.widget_filter.resize(100, 30 * (len(FILTER_TYPE) + len(GENRES)))

        self.widget_sorted.setStyleSheet("background-color: rgb(255, 0, 0); "
                                         "border-color: rgb(255, 255, 255);")
        self.widget_filter.setStyleSheet("background-color: rgb(255, 0, 0); "
                                         "border-color: rgb(255, 255, 255);")

        self.widget_sorted.move(self.button_sorted.x(), self.button_sorted.y() + 25)
        self.widget_filter.move(self.button_filter.x(), self.button_filter.y() + 25)


    def reset_list(self):
        films = []
        text = self.search.text().lower()

        for i in self.film:
            flag = 1

            if i[4] not in self.genres:
                flag = 0
            if i[3] not in self.types:
                flag = 0

            if text != '':
                if text not in i[1].lower():
                    flag = 0

            if flag:
                films.append(i)

        print(123)

        self.films = films[:]

        if self.sortedFilm == 'Aa':
            self.films = sorted(self.films, key=lambda x: x[0])

        elif self.sortedFilm == 'El':
            self.films = sorted(self.films, key=lambda x: x[5])[::-1]












