import os
import sqlite3
import sys
import zipfile
import shutil

import PIL
from PIL import Image, ImageFilter
import sqlite3 as lite
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QColorDialog, QGridLayout, QLabel, QWidget, \
    QTableWidgetItem, QInputDialog


class Story_img(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('story_window.ui', self)
        self.button_1.clicked.connect(self.run)
        self.button_2.clicked.connect(self.run)
        self.connection = sqlite3.connect("image_story.sqlite")
        self.z = zipfile.ZipFile("spam.zip", 'r')
        self.table()

    def table(self):
        res = self.connection.cursor().execute("SELECT * FROM images").fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["im_id", "act", "im_name"])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def run(self):
        sender = self.sender().text()

        if sender == "Показать":
            if self.id.text().isdigit():
                n = self.id.text()
                self.conn = sqlite3.connect('image_story.sqlite').cursor().execute("SELECT im_name FROM images WHERE im_id = ?", (str(n)))
                name = [i[0] for i in self.conn][0]
                img = Image.open(self.z.extract(name))
                resized_img = img.resize((409, 423), Image.ANTIALIAS)
                resized_img.save('miniature.jpg')
                self.label.setPixmap(QPixmap('miniature.jpg'))
                # 405 390
            else:
                self.id.setText('Нормальное id напиши')


        elif sender == "Выбрать":
            print("выбрать")

        elif sender == 'Обновить':
            self.table()


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
        self.setGeometry(0, 0, 0, 0)


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
        self.conn = sqlite3.connect("image_story.sqlite")

        for i in range(1, 17):
            self.but = eval(f'self.button_{i}')
            self.but.clicked.connect(self.run)

    def save_picture(self, act='Начало'):

        with zipfile.ZipFile('spam.zip', 'a') as myzip:
            shutil.copy('rd_imm.jpg', 'rd_imm_{}.jpg'.format(self.times))
            myzip.write('rd_imm_{}.jpg'.format(self.times))
            os.remove('rd_imm_{}.jpg'.format(self.times))
        n = self.times
        self.conn.cursor().execute("INSERT INTO images VALUES (?, ?, ?);", (self.times,act,'rd_imm_{}.jpg'.format(self.times)))
        self.conn.commit()

    def how_many_times(self, new=False):

        self.times += 1

        if new:
            self.times = 0

        self.schet.display(self.times)

    def run(self):

        sender = self.sender().text()

        if sender == 'SOS' and self.allowed:

            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'По часовой' and self.allowed:

            if self.n + 90 > 360:
                self.n = 90
            else:
                self.n += 90

            t = QTransform().rotate(+90)
            self.imm = QPixmap('rd_imm.jpg').transformed(t)
            self.imm.save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('По часовой')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Против часовой' and self.allowed:

            if self.n - 90 < -360:
                self.n = -90
            else:
                self.n -= 90

            t = QTransform().rotate(-90)
            self.imm = QPixmap('rd_imm.jpg').transformed(t)
            self.imm.save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Против часовой')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Развернуть' and self.allowed:

            Image.open('rd_imm.jpg').transpose(Image.FLIP_LEFT_RIGHT).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Развернуть')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


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
            self.how_many_times()
            self.save_picture('Покрасить изображение')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.completed = 0
            self.progress.setValue(self.completed)
            self.hide()
            self.show()


        elif sender == 'Размытие' and self.allowed:

            Image.open().filter(ImageFilter.BLUR).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Размытие')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Резкость' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.SHARPEN).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Резкость')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Детализация' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.DETAIL).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Детализация')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Агрессивная детализация' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.EDGE_ENHANCE).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Агрессивная детализация')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Серые будни' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.EMBOSS).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Серые будни')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Мягкое размытие' and self.allowed:

            Image.open('rd_imm.jpg').filter(ImageFilter.SMOOTH).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Мягкое размытие')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


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

                for i in range(1, 17):
                    self.but = eval(f'self.button_{i}')
                    self.but.setStyleSheet('background: rgb{};'.format(colour))

                for i in range(1, 7):
                    self.lab = eval(f'self.label_{i}')
                    self.lab.setStyleSheet('background: rgb{};'.format(colour))


        elif sender == 'Выбрать Изображение':

            self.imm = QFileDialog.getOpenFileName(self, 'Выбрать фотокарточку', '', )[0]
            Image.open(self.imm).save('rd_imm.jpg')

            with zipfile.ZipFile('spam.zip', 'w') as myzip:
                pass

            self.conn.cursor().execute("DELETE FROM images")
            self.allowed = True
            self.how_many_times(True)
            self.save_picture()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()

        elif sender == 'История изменений':

            self.story_img = Story_img()
            self.story_img.show()

        elif sender == 'Сохранить':

            print('work')
            text, ok = QInputDialog.getText(self, 'Ввод', 'Название изображения')
            name = f'{text}.jpg'

            dlg = QFileDialog.getExistingDirectory(self,"Выбрать папку",".")
            print(f'{dlg}/{name}')
            Image.open('rd_imm.jpg').save(dlg)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
