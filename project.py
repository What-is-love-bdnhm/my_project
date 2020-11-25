import sqlite3
import sys

import PIL
from PIL import Image, ImageFilter
import sqlite3 as lite
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QColorDialog, QGridLayout, QLabel, QWidget


class Rdimm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle("Изображение")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.label = QLabel(self)
        self.label.move(0, 0)
        self.new_size()
        self.grid = QGridLayout(self.centralwidget)
        self.grid.addWidget(self.label)
        self.show()

    def new_size(self):
        self.imm = Image.open('rd_imm.jpg')
        self.x, self.y = self.imm.size
        if self.imm.width > 1920 or self.imm.height > 1080:
            self.x, self.y = 1920, 1080
            self.imm.thumbnail((1920, 1080), PIL.Image.ANTIALIAS)
            self.imm.save('rd_imm.jpg')
        self.label.resize(self.x, self.y)
        self.label.setPixmap(QPixmap('rd_imm.jpg'))
        self.setGeometry(0,0,0,0)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test_qt.ui', self)
        self.setWindowTitle('Демо-фотошоп')
        self.pixmap = QPixmap("rd_imm.jpg")

        self.n = 0
        self.times = 0
        self.completed = 0
        self.allowed = False

        self.button_1.clicked.connect(self.run)
        self.button_2.clicked.connect(self.run)
        self.button_3.clicked.connect(self.run)
        self.button_4.clicked.connect(self.run)
        self.button_5.clicked.connect(self.run)
        self.button_6.clicked.connect(self.run)
        self.button_7.clicked.connect(self.run)
        self.button_8.clicked.connect(self.run)
        self.button_9.clicked.connect(self.run)
        self.button_10.clicked.connect(self.run)
        self.button_11.clicked.connect(self.run)
        self.button_12.clicked.connect(self.run)
        self.button_13.clicked.connect(self.run)
        self.button_14.clicked.connect(self.run)
        self.button_15.clicked.connect(self.run)


    def read_picture(self):

        con = sqlite3.connect('story_of_img.sqlite')
        cur = con.cursor()


    def how_many_times(self, new=False):

        self.times += 1

        if new:
            self.times = 0

        self.schet.display(self.times)


    def run(self):

        sender = self.sender().text()

        if sender == 'История изменений' and self.allowed:

            pass

        elif sender == 'SOS' and self.allowed:

            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()


        elif sender == 'По часовой' and self.allowed:

            if self.n + 90 > 360:
                self.n = 90
            else:
                self.n += 90

            t = QTransform().rotate(+90)
            self.imm = QPixmap('rd_imm.jpg').transformed(t)
            self.imm.save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Против часовой' and self.allowed:

            if self.n - 90 < -360:
                self.n = -90
            else:
                self.n -= 90

            t = QTransform().rotate(-90)
            self.imm = QPixmap('rd_imm.jpg').transformed(t)
            self.imm.save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Развернуть' and self.allowed:

            Image.open("rd_imm.jpg").transpose(Image.FLIP_LEFT_RIGHT).save("rd_imm.jpg")
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Покрасить изображение' and self.allowed:

            color = QColorDialog.getColor()
            color = color.name().lstrip('#')
            lv = len(color)
            colour = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            source = Image.open('rd_imm.jpg')
            result = Image.new('RGB', source.size)
            percent = 100 / (source.width * source.height)

            for x in range(source.size[0]):
                for y in range(source.size[1]):
                    r, g, b = source.getpixel((x, y))
                    red = int((r + colour[0]) / 2)
                    green = int((g + colour[1]) / 2)
                    blue = int((b + colour[2]) / 2)
                    result.putpixel((x, y), (red, green, blue))
                    self.completed += percent
                    self.progress.setValue(self.completed)

            result.save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.completed = 0
            self.progress.setValue(self.completed)
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Размытие' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.BLUR).save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Резкость' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.SHARPEN).save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Детализация' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.DETAIL).save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Агрессивная детализация' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.EDGE_ENHANCE).save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Серые будни' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.EMBOSS).save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Мягкое размытие' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.SMOOTH).save('rd_imm.jpg')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()
            self.how_many_times()


        elif sender == 'Сменить фон':

            color = QColorDialog.getColor()

            if color.isValid():
                self.setStyleSheet("background-color: {}".format(color.name()))
                color = color.name().lstrip('#')
                lv = len(color)
                colour = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
                colour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                if colour[0] <= 30 and colour[1] <= 30 and colour[2] <= 30:
                    colour = (230, 230, 230)
                for i in range(1, 16):
                    self.but = eval(f'self.button_{i}')
                    self.but.setStyleSheet('background: rgb{};'.format(colour))
                for i in range(1, 6):
                    self.lab = eval(f'self.label_{i}')
                    self.lab.setStyleSheet('background: rgb{};'.format(colour))


        elif sender == 'Выбрать Изображение':

            self.imm = QFileDialog.getOpenFileName(self, 'Выбрать фотокарточку', '',)[0]
            Image.open(self.imm).save('rd_imm.jpg')

            self.allowed = True
            self.how_many_times(True)
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
