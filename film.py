from PyQt6.QtWidgets import QPushButton, QLineEdit, QMainWindow, QWidget, QCheckBox, QListWidget, QLabel, QTextEdit, \
    QRadioButton, QSlider
from PyQt6.QtCore import QRect, Qt, QMargins
from consts import FILTER_TYPE, SORTED_TYPE, GENRES
from PyQt6.QtGui import QFont, QTextBlockFormat


class Film(QMainWindow):
    def __init__(self, width, height, widget):
        super(Film, self).__init__(widget)

        self.setGeometry(QRect(300, 200, width - 600, height - 400))
        self.setStyleSheet("border-image: url(redBackground.jpg) 0 0 0 0  ;")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.cur = widget.cur
        self.con = widget.con
        self.width = width
        self.height = height
        self.widget = widget
        self.id = -1
        self.families = widget.families

        self.listFilmsAll = list(self.cur.execute(f'''SELECT title, info, type, genre, estimation FROM films'''))
        self.dictGenres = {i: j for i, j in list(self.cur.execute(f'''SELECT id, title FROM genres'''))}
        self.dictTypes = {i: j for i, j in list(self.cur.execute(f'''SELECT id, title FROM types'''))}

        self.back = QPushButton(self)
        self.back.move(10, 10)
        self.back.resize(81, 81)
        self.back.setStyleSheet("QPushButton{border-image: url(back.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(backHover.png) 0 0 0 0  ;}")
        self.back.clicked.connect(self.backFunc)

        self.edit = QCheckBox(self)
        self.edit.move(1000, 10)
        self.edit.resize(81, 81)
        self.edit.setStyleSheet("QCheckBox{border-image: url(edit.png) 0 0 0 0  ; color: #ff384d; }"
                                "QCheckBox:hover{border-image: url(editHover.png) 0 0 0 0  ;}"
                                "QCheckBox:checked{border-image: url(editHover.png) 0 0 0 0  ;}"
                                "QCheckBox::indicator {width: 81px;height: 81px; image: url(0.png);}")
        self.edit.clicked.connect(self.editFunc)

        self.info = QTextEdit(self)
        self.info.move(1000, 200)
        self.info.resize(700, 400)
        self.info.setFont(QFont(self.families[0], 18))
        self.info.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.info.setStyleSheet("QTextEdit{border-image: url(19.png) 20 15 20 15 ; padding: 10px;"
                                "color: #000000; border-radius: 5px;}")
        self.info.setReadOnly(1)

        self.card = QLabel(self)
        self.card.move(350, 200)
        self.card.resize(440, 700)
        self.card.setStyleSheet("border-image: url(card.png) 0 0 0 0;")

        self.lable = QTextEdit("Название", self.card)
        self.lable.move(80, 430)
        self.lable.resize(340, 120)
        self.lable.setStyleSheet("border-image: url(0.png) 0 0 0 0;")
        self.lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lable.setFont(QFont(self.families[0], 30))
        self.lable.setReadOnly(1)

        typeTitle = QLabel("Тип:", self.card)
        typeTitle.move(40, 544)
        typeTitle.resize(130, 40)
        typeTitle.setFont(QFont(self.families[0], 24))
        typeTitle.setStyleSheet("border-image: url(0.png) 0 0 0 0; ")

        self.type = QLabel(self.dictTypes[1], self.card)
        self.type.move(180, 544)
        self.type.resize(360, 40)
        self.type.setFont(QFont(self.families[0], 24))
        self.type.setStyleSheet("border-image: url(0.png) 0 0 0 0; ")

        generTitle = QLabel("Жанр:", self.card)
        generTitle.move(40, 584)
        generTitle.resize(130, 40)
        generTitle.setFont(QFont(self.families[0], 24))
        generTitle.setStyleSheet("border-image: url(0.png) 0 0 0 0; ")

        self.genre = QLabel(self.dictGenres[1], self.card)
        self.genre.move(180, 584)
        self.genre.resize(360, 40)
        self.genre.setFont(QFont(self.families[0], 24))
        self.genre.setStyleSheet("border-image: url(0.png) 0 0 0 0; ")

        ratingTitle = QLabel("Рейтинг:", self.card)
        ratingTitle.move(40, 624)
        ratingTitle.resize(130, 40)
        ratingTitle.setFont(QFont(self.families[0], 24))
        ratingTitle.setStyleSheet("border-image: url(0.png) 0 0 0 0; ")

        self.rating = QLabel('5.0', self.card)
        self.rating.move(180, 624)
        self.rating.resize(360, 40)
        self.rating.setFont(QFont(self.families[0], 24))
        self.rating.setStyleSheet("border-image: url(0.png) 0 0 0 0; ")

        self.checkType = QCheckBox(self)
        self.checkType.move(1120, 620)
        self.checkType.resize(81, 81)
        self.checkType.setStyleSheet("QCheckBox{border-image: url(type.png) 0 0 0 0  ; color: #ff384d; }"
                                "QCheckBox:hover{border-image: url(typeHover.png) 0 0 0 0  ;}"
                                "QCheckBox:checked{border-image: url(typeHover.png) 0 0 0 0  ;}"
                                "QCheckBox::indicator {width: 81px;height: 81px; image: url(0.png);}")
        self.checkType.clicked.connect(self.typeFunc)

        self.checkGenre = QCheckBox(self)
        self.checkGenre.move(1320, 620)
        self.checkGenre.resize(81, 81)
        self.checkGenre.setStyleSheet("QCheckBox{border-image: url(genre.png) 0 0 0 0  ; color: #ff384d; }"
                                     "QCheckBox:hover{border-image: url(genreHover.png) 0 0 0 0  ;}"
                                     "QCheckBox:checked{border-image: url(genreHover.png) 0 0 0 0  ;}"
                                     "QCheckBox::indicator {width: 81px;height: 81px; image: url(0.png);}")
        self.checkGenre.clicked.connect(self.genreFunc)

        self.image = QPushButton(self)
        self.image.move(1520, 620)
        self.image.resize(81, 81)
        self.image.setStyleSheet("QPushButton{border-image: url(image.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(imageHover.png) 0 0 0 0  ;}")
        self.image.clicked.connect(self.imageFunc)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.slideEdit)
        self.slider.move(1120, 750)
        self.slider.resize(481, 30)
        self.slider.setStyleSheet('border-image: url(0.png) 0 0 0 0;')

        self.checkType.setEnabled(False)
        self.checkGenre.setEnabled(False)
        self.image.setEnabled(False)
        self.slider.setEnabled(False)

        self.arrTypeRadio = []
        self.arrGenreRadio = []

        self.typeWidget = QWidget(self)
        self.typeWidget.move(1120, 721)
        self.typeWidget.resize(200, 40 + 50 * len(self.dictTypes))
        self.typeWidget.setStyleSheet('border-image: url(greenBackground.png) 0 0 0 0  ;')
        self.typeWidget.hide()

        y = 40
        for i in self.dictTypes:
            radio = QRadioButton(self.dictTypes[i], self.typeWidget)
            radio.move(15, y)
            radio.resize(150, 30)
            radio.setFont(QFont(self.families[0], 14))
            radio.setStyleSheet('''QRadioButton::indicator:checked {image: url(radioHave.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:checked:hover {image: url(radioHaveHover.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:unchecked {image: url(radioEmpty.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:unchecked:hover {image: url(radioEmptyHover.png) 0 0 0 0  ;}
                                    QRadioButton{border-image: url(0.png);}''')
            self.arrTypeRadio.append(radio)
            radio.clicked.connect(self.editTypes)
            if i == 1:
                radio.click()
            y += 40

        self.genreWidget = QWidget(self)
        self.genreWidget.move(1320, 721)
        self.genreWidget.resize(200, 40 + 50 * len(self.dictGenres))
        self.genreWidget.setStyleSheet('border-image: url(greenBackground.png) 0 0 0 0  ;')
        self.genreWidget.hide()

        y = 40
        for i in self.dictGenres:
            radio = QRadioButton(self.dictGenres[i], self.genreWidget)
            radio.move(15, y)
            radio.resize(150, 30)
            radio.setFont(QFont(self.families[0], 14))
            radio.setStyleSheet('''QRadioButton::indicator:checked {image: url(radioHave.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:checked:hover {image: url(radioHaveHover.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:unchecked {image: url(radioEmpty.png) 0 0 0 0  ;}
                                    QRadioButton::indicator:unchecked:hover {image: url(radioEmptyHover.png) 0 0 0 0  ;}
                                    QRadioButton{border-image: url(0.png);}''')
            self.arrGenreRadio.append(radio)
            radio.clicked.connect(self.editGenres)
            if i == 1:
                radio.click()
            y += 40

        self.save = QPushButton(self)
        self.save.move(1619, 10)
        self.save.resize(81, 81)
        self.save.setStyleSheet("QPushButton{border-image: url(save.png) 0 0 0 0  ; color: #ff384d;}"
                                "QPushButton:hover{border-image: url(saveHover.png) 0 0 0 0  ;}")
        self.save.clicked.connect(self.saveFunc)

    def saveFunc(self):
        title = self.lable.toPlainText()
        info = self.info.toPlainText()
        type = [i.text() for i in self.arrTypeRadio if i.isChecked()][0]
        genre = [i.text() for i in self.arrGenreRadio if i.isChecked()][0]
        estimation = int(float(self.rating.text()) * 10)

        if self.id == -1:
            id = len(self.listFilmsAll) + 1

            self.cur.execute(f"""INSERT INTO films(id, title, info, type, genre, estimation)
                                                    VALUES ({id}, '{title}', '{info}', 
                                                    (SELECT id FROM types WHERE title = '{type}'), 
                                                    (SELECT id FROM genres WHERE title = '{genre}'), {estimation})""")
            self.id = id
        else:
            self.cur.execute(f"""UPDATE films SET title = '{title}', info = '{info}',
                                type = (SELECT id FROM types WHERE title = '{type}'),
                                genre = (SELECT id FROM genres WHERE title = '{genre}'),
                                estimation = {estimation}
                                WHERE id = '{self.id}'""")

        self.con.commit()

        self.listFilmsAll = list(self.cur.execute(f'''SELECT title, info, type, genre, estimation FROM films'''))
        self.watch.listFilmsAll = self.listFilmsAll[:]
        self.watch.updateFilter()

    def slideEdit(self):
        self.rating.setText(str(self.slider.value() / 10))

    def typeFunc(self):
        if self.checkType.isChecked():
            if self.checkGenre.isChecked():
                self.checkGenre.click()
            self.typeWidget.show()
        else:
            self.typeWidget.hide()

    def genreFunc(self):
        if self.checkGenre.isChecked():
            if self.checkType.isChecked():
                self.checkType.click()
            self.genreWidget.show()
        else:
            self.genreWidget.hide()

    def imageFunc(self):
        pass

    def editTypes(self):
        s = ''
        for i in self.arrTypeRadio:
            if i.isChecked():
                s = i.text()
                break
        self.type.setText(s)

    def editGenres(self):
        s = ''
        for i in self.arrGenreRadio:
            if i.isChecked():
                s = i.text()
                break
        self.genre.setText(s)

    def backFunc(self):
        self.hide()

    def editFunc(self):
        if self.edit.isChecked():
            self.info.setReadOnly(0)
            self.lable.setReadOnly(0)

            if self.checkGenre.isChecked():
                self.checkGenre.click()
            if self.checkType.isChecked():
                self.checkType.click()

            self.checkType.setEnabled(True)
            self.checkGenre.setEnabled(True)
            self.image.setEnabled(True)
            self.slider.setEnabled(True)
        else:
            self.info.setReadOnly(1)
            self.lable.setReadOnly(1)

            if self.checkGenre.isChecked():
                self.checkGenre.click()
            if self.checkType.isChecked():
                self.checkType.click()

            self.checkType.setEnabled(False)
            self.checkGenre.setEnabled(False)
            self.image.setEnabled(False)
            self.slider.setEnabled(False)


    def resetId(self, id, watch):
        self.watch = watch
        self.id = id
        if self.id == -1:
            self.lable.setText('Название')
            self.lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if self.edit.isChecked():
                self.edit.click()
            self.arrTypeRadio[0].click()
            self.arrGenreRadio[0].click()
            self.info.setText('')
            self.slider.setValue(50)
            self.rating.setText('5.0')
        else:
            s = list(self.cur.execute(f'''SELECT title, info, type, genre, estimation FROM films
                                        WHERE id == "{self.id}"'''))[0]
            self.lable.setText(s[0])
            self.lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if self.edit.isChecked():
                self.edit.click()
            self.arrTypeRadio[s[2] - 1].click()
            self.arrGenreRadio[s[3] - 1].click()
            self.info.setText(s[1])
            self.slider.setValue(s[4])
            self.rating.setText(str(s[4] / 10))