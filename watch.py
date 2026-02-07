from PyQt6.QtWidgets import QPushButton, QLineEdit, QMainWindow, QWidget, QCheckBox, QListWidget, QLabel, QRadioButton
from PyQt6.QtCore import QRect, Qt, QThread, pyqtSignal
from consts import FILTER_TYPE, SORTED_TYPE, GENRES, DICT_FILTER, DICT_GENRES, DICT_FILTER_NUM, DICT_GENRES_NUM
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QKeyEvent
from film import Film
from PyQt6 import QtCore

class Watch(QMainWindow):
    def __init__(self, width, height, widget):
        super(Watch, self).__init__(widget)

        self.setGeometry(QRect(300, 200, width - 600, height - 400))
        self.setStyleSheet("border-image: url(6.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.cur = widget.cur
        self.con = widget.con
        self.width = width
        self.height = height
        self.widget = widget
        self.film = widget.film

        id = QFontDatabase.addApplicationFont("LeticeaBumsteadCyrillic.otf")
        self.families = QFontDatabase.applicationFontFamilies(id)

        self.up = QPushButton(self)
        self.up.move(10, 100)
        self.up.clicked.connect(self.upFunc)
        self.up.setStyleSheet("QPushButton{border-image: url(back.png) 0 0 0 0  ; color: #ff384d;}"
                                 "QPushButton:hover{border-image: url(backHover.png) 0 0 0 0  ;}")

        self.down = QPushButton(self)
        self.down.move(10, 150)
        self.down.setStyleSheet("QPushButton{border-image: url(back.png) 0 0 0 0  ; color: #ff384d;}"
                                 "QPushButton:hover{border-image: url(backHover.png) 0 0 0 0  ;}")
        self.down.clicked.connect(self.downFunc)

        self.nowStage = 0

        self.setStyleSheet("border-image: url(blueBackground.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.back = QPushButton(self)
        self.back.move(10, 10)
        self.back.resize(81, 81)
        self.back.setStyleSheet("QPushButton{border-image: url(back.png) 0 0 0 0  ; color: #ff384d;}"
                                 "QPushButton:hover{border-image: url(backHover.png) 0 0 0 0  ;}")
        self.back.clicked.connect(self.backFunc)

        self.filter = QCheckBox(self)
        self.filter.move(1261, 10)
        self.filter.resize(81, 81)
        self.filter.setStyleSheet("QCheckBox{border-image: url(filter.png) 0 0 0 0  ; color: #ff384d;}"
                                "QCheckBox:hover{border-image: url(filterHover.png) 0 0 0 0  ;}"
                                "QCheckBox:checked{border-image: url(filterHover.png) 0 0 0 0  ;}"  
                                "QCheckBox::indicator {width: 81px;height: 81px; image: url(0.png);}")
        self.filter.clicked.connect(self.filterFunc)

        self.sort = QCheckBox(self)
        self.sort.move(1170, 10)
        self.sort.resize(81, 81)
        self.sort.setStyleSheet("QCheckBox{border-image: url(sort.png) 0 0 0 0  ; color: #ff384d; }"
                                "QCheckBox:hover{border-image: url(sortHover.png) 0 0 0 0  ;}"
                                "QCheckBox:checked{border-image: url(sortHover.png) 0 0 0 0  ;}"
                                "QCheckBox::indicator {width: 81px;height: 81px; image: url(0.png);}")
        self.sort.clicked.connect(self.sortFunc)

        self.plus = QPushButton(self)
        self.plus.move(609, 10)
        self.plus.resize(81, 81)
        self.plus.setStyleSheet("QPushButton{border-image: url(plus.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(plusHover.png) 0 0 0 0  ;}")
        self.plus.clicked.connect(self.plusFunc)

        self.find = QLineEdit(self)
        self.find.move(700, 10)
        self.find.resize(460, 81)
        self.find.setFont(QFont(self.families[0], 19))
        self.find.setTextMargins(25, 0, 80, 0)
        self.find.setStyleSheet("QLineEdit{border-image: url(find.png) 0 0 0 0  ; color: #000000;}"
                                "QLineEdit:hover{border-image: url(findHover.png) 0 0 0 0  ;}")
        self.find.textChanged.connect(self.updateFilter)

        self.listFilms = list(self.cur.execute(f'''SELECT title, info, type, genre, estimation FROM films'''))
        self.listFilmsAll = self.listFilms[:]
        self.dictGenres = {i: j for i, j in list(self.cur.execute(f'''SELECT id, title FROM genres'''))}
        self.dictTypes = {i: j for i, j in list(self.cur.execute(f'''SELECT id, title FROM types'''))}

        self.listDistributionFilms = []
        self.arrButtons = self.createButtons()
        self.createListD()

        self.filterWidget = QWidget(self)
        self.filterWidget.move(1261, 101)
        self.filterWidget.resize(200, 80 + 50 * (len(self.dictTypes) + len(self.dictGenres)))
        self.filterWidget.setStyleSheet('border-image: url(greenBackground.png) 0 0 0 0  ;')
        self.filterWidget.hide()
        lable = QLabel('Тип:', self.filterWidget)
        lable.move(15, 20)
        lable.resize(150, 40)
        lable.setFont(QFont(self.families[0], 17))
        lable.setStyleSheet('border-image: url(0.png);')

        self.arrGenreCheck = []
        self.arrTypeCheck = []
        self.arrSortRadio = []

        y = 60
        for i in self.dictTypes:
            check = QCheckBox(self.dictTypes[i], self.filterWidget)
            check.move(15, y)
            check.resize(150, 30)
            check.setFont(QFont(self.families[0], 14))
            check.setStyleSheet('''QCheckBox::indicator:checked {image: url(checkHave.png) 0 0 0 0  ;}
                                   QCheckBox::indicator:checked:hover {image: url(checkHaveHover.png) 0 0 0 0  ;}
                                   QCheckBox::indicator:unchecked {image: url(checkEmpty.png) 0 0 0 0  ;}
                                   QCheckBox::indicator:unchecked:hover {image: url(checkEmptyHover.png) 0 0 0 0  ;}
                                   QCheckBox{border-image: url(0.png);}''')
            self.arrTypeCheck.append(check)
            check.click()
            check.clicked.connect(self.updateFilter)
            y += 40

        lableg = QLabel('Жанр:', self.filterWidget)
        lableg.move(15, y)
        lableg.resize(150, 40)
        lableg.setFont(QFont(self.families[0], 17))
        lableg.setStyleSheet('border-image: url(0.png);')

        y += 40
        for i in self.dictGenres:
            check = QCheckBox(self.dictGenres[i], self.filterWidget)
            check.move(15, y)
            check.resize(150, 40)
            check.setStyleSheet('')
            check.setFont(QFont(self.families[0], 14))
            check.setStyleSheet('''QCheckBox::indicator:checked {image: url(checkHave.png) 0 0 0 0  ;}
                                    QCheckBox::indicator:checked:hover {image: url(checkHaveHover.png) 0 0 0 0 ;}
                                    QCheckBox::indicator:unchecked {image: url(checkEmpty.png) 0 0 0 0  ;}
                                    QCheckBox::indicator:unchecked:hover {image: url(checkEmptyHover.png) 0 0 0 0  ;}
                                    QCheckBox{border-image: url(0.png);}''')
            self.arrGenreCheck.append(check)
            check.click()
            check.clicked.connect(self.updateFilter)
            y += 40

        self.sortWidget = QWidget(self)
        self.sortWidget.move(1170, 101)
        self.sortWidget.resize(200, 40 + 35 * len(SORTED_TYPE))
        self.sortWidget.setStyleSheet('border-image: url(greenBackground.png) 0 0 0 0  ;')
        self.sortWidget.hide()

        y = 15
        for i in SORTED_TYPE:
            radio = QRadioButton(i, self.sortWidget)
            radio.move(15, y)
            radio.resize(150, 40)
            radio.setStyleSheet('')
            radio.setFont(QFont(self.families[0], 14))
            radio.setStyleSheet('''QRadioButton::indicator:checked {image: url(radioHave.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:checked:hover {image: url(radioHaveHover.png) 0 0 0 0 ;}
                                    QRadioButton::indicator:unchecked {image: url(radioempty.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:unchecked:hover {image: url(radioEmptyHover.png) 0 0 0 0  ;}
                                    QRadioButton{border-image: url(0.png);}''')
            self.arrSortRadio.append(radio)
            radio.clicked.connect(self.updateSort)
            if i == SORTED_TYPE[0]:
                radio.click()
            y += 40

        self.editButtons()

        print(*self.listDistributionFilms, sep='\n')

    def edit(self):
        title = [i[1].text() for i in self.arrButtons if i[0] == self.sender()][0]
        id = list(self.cur.execute(f'''SELECT id FROM films WHERE title == "{title}"'''))[0][0]
        self.film.resetId(id, self)
        self.film.show()

    def findFunc(self):
        s = self.find.text()
        arr = []
        for i in self.listFilms:
            if s in i[0]:
                arr.append(i)
        self.listFilms = arr[:]
        self.updateSort()

    def updateFilter(self):
        self.nowStage = 0
        types = []
        geners = []
        for en, i in enumerate(self.arrTypeCheck):
            if i.isChecked():
                types.append(en + 1)
        for en, i in enumerate(self.arrGenreCheck):
            if i.isChecked():
                geners.append(en + 1)
        self.listFilms = []
        for i in self.listFilmsAll:
            if i[2] in types and i[3] in geners:
                self.listFilms.append(i)
        self.findFunc()

    def updateSort(self):
        for i in self.arrSortRadio:
            if i.isChecked():
                if i.text() == SORTED_TYPE[0]:
                    self.listFilms = sorted(self.listFilms, key=lambda x: x[0])
                else:
                    self.listFilms = sorted(self.listFilms, key=lambda x: x[4])[::-1]
        self.createListD()

    def editButtons(self):
        for i in range(10):
            button = self.arrButtons[i][0]
            if len(self.listDistributionFilms) != 0 and len(self.listDistributionFilms[self.nowStage]) > i:
                button.show()

                types = self.dictTypes[self.listDistributionFilms[self.nowStage][i][2]]
                genres = self.dictGenres[self.listDistributionFilms[self.nowStage][i][3]]

                self.arrButtons[i][1].setText(self.listDistributionFilms[self.nowStage][i][0])
                self.arrButtons[i][2].setText(f'Тип: {types}')
                self.arrButtons[i][3].setText(f'Жанр: {genres}')
                self.arrButtons[i][4].setText(f'Рейтинг: {str(self.listDistributionFilms[self.nowStage][i][4] / 10)}')

            else:
                button.hide()

    def sortFunc(self):
        if self.sort.isChecked():
            if self.filter.isChecked():
                self.filter.click()
            self.sortWidget.show()
        else:
            self.sortWidget.hide()

    def filterFunc(self):
        if self.filter.isChecked():
            if self.sort.isChecked():
                self.sort.click()
            self.filterWidget.show()
        else:
            self.filterWidget.hide()

    def plusFunc(self):
        self.film.resetId(-1, self)
        self.film.show()


    def createListD(self):
        if len(self.listFilms) != 0:
            self.listDistributionFilms = [self.listFilms[i * 10:i * 10 + 10] for i in range(len(self.listFilms) // 10)]
            if len(self.listFilms) % 10 != 0:
                self.listDistributionFilms.append(self.listFilms[len(self.listFilms) // 10 * 10:])
        else:
            self.listDistributionFilms = []
        self.editButtons()

    def backFunc(self):
        self.hide()

    def createButtons(self):
        y = 200
        arr = []
        for i in range(2):
            x = 260
            for j in range(5):
                button = QPushButton(self)
                button.resize(220, 350)
                button.move(x, y)
                button.setStyleSheet("QPushButton{border-image: url(card.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(cardHover.png) 0 0 0 0  ;}")

                lable = QLabel('', button)
                lable.move(40, 220)
                lable.resize(170, 45)
                lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lable.setWordWrap(1)
                lable.setFont(QFont(self.families[0], 15))

                types = QLabel('', button)
                types.move(20, 272)
                types.resize(180, 20)
                types.setFont(QFont(self.families[0], 12))

                genres = QLabel('', button)
                genres.move(20, 292)
                genres.resize(180, 20)
                genres.setFont(QFont(self.families[0], 12))

                rating = QLabel('', button)
                rating.move(20, 312)
                rating.resize(180, 20)
                rating.setFont(QFont(self.families[0], 12))



                x += 300

                button.clicked.connect(self.edit)

                arr.append([button, lable, types, genres, rating])
            y += 400
        return arr

    def downFunc(self):
        if self.nowStage + 1 != len(self.listDistributionFilms):
            self.nowStage += 1
        self.editButtons()

    def upFunc(self):
        if self.nowStage != 0:
            self.nowStage -= 1
        self.editButtons()

