# Основное окно Example находится в самом низу
import os
import sqlite3
import sys
import zipfile
import shutil

import PIL
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QColorDialog, QGridLayout, QLabel, QWidget, \
    QTableWidgetItem, QInputDialog

# окно отвечающее за возможность взаимодействия с историей редактирования
class Story_img(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('story_window.ui', self)
        self.setWindowTitle("История изменений")
        self.button_1.clicked.connect(self.run)
        self.button_2.clicked.connect(self.run)
        # подключение к базе данных с информацией о изображениях
        self.connection = sqlite3.connect("image_story.sqlite")
        # открывается архив с редактированными изображениями
        self.z = zipfile.ZipFile("spam.zip", 'r')

        self.table()

    # функция создания таблицы в окне. здесь показывается вся история изображений
    def table(self):
        # уже знакомый из прошлых уроков способ написания таблицы

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

    # собранные воедино функции, вызывающиеся по названию кнопки
    def run(self):

        # ловим текст из нажатой пользователем кнопки
        sender = self.sender().text()

        # функция дает возможность предпросмотра выбранного изображения
        if sender == "Показать":
            # для начала идет проверка на корректность написанного id
            if self.id.text().isdigit():
                # в переменную записывается написанное в Qlabel число
                n = self.id.text()
                # небольшая проверка на корректность id
                if len(self.z.namelist()) < int(n):
                    self.id.setText('Нормальное id напиши')
                    return
                # берётся название изображения с соответсвующим id
                self.conn = sqlite3.connect('image_story.sqlite').cursor().\
                execute("SELECT im_name FROM images WHERE im_id = ?", (str(n)))
                # название записывается в переменную
                name = [i[0] for i in self.conn][0]
                # берётся изображение из архива
                img = Image.open(self.z.extract(name))
                # масштабируется под размеры qpixmap
                resized_img = img.resize((409, 423), Image.ANTIALIAS)
                # сохраняется и соответственно вставляется в qpixmap
                resized_img.save('miniature.jpg')
                self.label.setPixmap(QPixmap('miniature.jpg'))
            else:
                self.id.setText('Нормальное id напиши')


        # аналогичная прошлой функция, но изображение забирается для дальнейшего редактирования
        elif sender == "Выбрать":
            self.conn = sqlite3.connect('image_story.sqlite')
            if self.id.text().isdigit():
                n = self.id.text()
                if len(self.z.namelist()) < int(n):
                    self.id.setText('Нормальное id напиши')
                    return
                img = self.conn.cursor().execute("SELECT im_name FROM images WHERE im_id = ?", (str(n)))
                name = [i[0] for i in img][0]
                img = Image.open(self.z.extract(name))
                # взятое их архива изображение заменяет редактируемое в настоящее время
                img.save('rd_imm.jpg')
                self.hide()
                # вызываем функцию из основного окна, передаем id взятого изображения
                ex.how_many_times(False, n)
            else:
                self.id.setText('Нормальное id напиши')





        elif sender == 'Обновить':
            pass
            # к сожалению автора настиг творческий кризис

# окно с редактируемым изображением
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

    # функция устанавливает размер окна равный размеру изображения
    def new_size(self):
        # берётся изображение
        self.imm = Image.open('rd_imm.jpg')
        # выясняются размеры
        self.x, self.y = self.imm.size
        # проверка на выход за размеры дисплея
        # в данном случае код рассчитан на ноутбуки, где разрешение равно показанному ниже
        if self.imm.width > 1920 or self.imm.height > 1080:
            # в случае выхода за размеры дисплея изображение масштабируется
            self.x, self.y = 1920, 1080
            # масштабирование под заданные размеры
            self.imm.thumbnail((1920, 1080), PIL.Image.ANTIALIAS)
            self.imm.save('rd_imm.jpg')
        self.label.resize(self.x, self.y)
        self.label.setPixmap(QPixmap('rd_imm.jpg'))
        self.setGeometry(0, 0, 0, 0)


# основное окно со всеми функциями
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test_qt.ui', self)
        self.setWindowTitle('Демо-фотошоп')
        self.pixmap = QPixmap("rd_imm.jpg")
        # номер редактированного изображения. нужен для удобства пользователем нахождения его в истории
        self.times = 0
        # количество процентов в статус-баре загрузки привязанном к покрасу
        self.completed = 0
        # разрешение на нажатие кнопок. разблокируется после вставки изображения
        self.allowed = False
        self.conn = sqlite3.connect("image_story.sqlite")

        # незамысловатое решение подключить уйму кнопок
        for i in range(1, 17):
            self.but = eval(f'self.button_{i}')
            self.but.clicked.connect(self.run)

    # функция сохраняет редактированные изображения в архив, дабы те не засоряли основную папку
    # вместе с тем в функцию передается название действия с изображением
    def save_picture(self, act='Начало'):

        # открывается архив
        with zipfile.ZipFile('spam.zip', 'a') as myzip:
            # создается копия редактированного изображения
            shutil.copy('rd_imm.jpg', 'rd_imm_{}.jpg'.format(self.times))
            # запись копии в архив
            myzip.write('rd_imm_{}.jpg'.format(self.times))
            # удаление копии из основной папки
            os.remove('rd_imm_{}.jpg'.format(self.times))
        # в базу данных сохраняются id, проделанное действие и название изображения
        self.conn.cursor().execute("INSERT INTO images VALUES (?, ?, ?);", (self.times, act, 'rd_imm_{}.jpg'.format(self.times)))
        self.conn.commit()

    # функция отвечает за изменение id
    def how_many_times(self, new=False, get=None):

        # после каждого вызова по окончанию работы фильтра, значение увеличивается для передачи следующему изображению
        self.times += 1

        # если было взято изображение из истории, то значение times меняется на соответсвующее число
        if get != None:
            print(get)
            self.times = int(get)

        # с каждой вставкой изображения счётчик обновляется
        if new:
            self.times = 0

        # отображение значения в lcdnumber
        self.schet.display(self.times)

    # собранные воедино функции, функционал отражают их названия
    def run(self):

        # ловим текст из нажатой пользователем кнопки
        sender = self.sender().text()

        # функция обновляет редактирующееся в данный момент изображение
        if sender == 'SOS':

            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'По часовой' and self.allowed:

            # функция поворота изображения берётся в переменную для удобства
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

            # функция поворота изображения берётся в переменную для удобства
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

            # изображение открывается и сразу трансформиуется по заданной функции
            Image.open('rd_imm.jpg').transpose(Image.FLIP_LEFT_RIGHT).save('rd_imm.jpg')
            self.how_many_times()
            self.save_picture('Развернуть')
            self.rdwindow.hide()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()


        elif sender == 'Покрасить изображение' and self.allowed:

            # берётся html код цвета из диалога
            color = QColorDialog.getColor()
            # <
            color = color.name().lstrip('#')
            lv = len(color)
            colour = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            # > действует формула из интернета. перевод из html в rgb
            source = Image.open('rd_imm.jpg')
            result = Image.new('RGB', source.size)
            # вычисляется прогресс в проценте при обработке одного пикселя
            percent = 100 / (source.width * source.height)

            # каждый пиксель окрашивается в выбранный цвет. взято из пройденного материала
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

            Image.open('rd_imm.jpg').filter(ImageFilter.BLUR).save('rd_imm.jpg')
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

            # берётся цвет из диалога
            color = QColorDialog.getColor()

            # проверяется корректность цвета
            if color.isValid():
                # задний фон сменяет цвет на выбранный
                self.setStyleSheet("background-color: {}".format(color.name()))
                # -
                color = color.name().lstrip('#')
                lv = len(color)
                colour = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
                # + взятая из интернета формула для перевода цвета из html в rgb
                # берётся инвертированный цвет
                colour = (255 - colour[0], 255 - colour[1], 255 - colour[2])

                # цвет проверяется на яркость, поскольку цвет кнопок и прочего инвертируется выбранному
                if colour[0] <= 30 and colour[1] <= 30 and colour[2] <= 30:
                    colour = (230, 230, 230)

                # окрашиваются кнопки
                for i in range(1, 17):
                    self.but = eval(f'self.button_{i}')
                    self.but.setStyleSheet('background: rgb{};'.format(colour))

                # окрашивается фон текста
                for i in range(1, 7):
                    self.lab = eval(f'self.label_{i}')
                    self.lab.setStyleSheet('background: rgb{};'.format(colour))


        elif sender == 'Выбрать Изображение':
            # диалог с выбором файла
            self.imm = QFileDialog.getOpenFileName(self, 'Выбрать фотокарточку', '', )[0]
            Image.open(self.imm).save('rd_imm.jpg')
            # создание архива для фотографий
            with zipfile.ZipFile('spam.zip', 'w') as myzip:
                pass
            # база данных полностью очищается
            self.conn.cursor().execute("DELETE FROM images")
            # дается разрешение на нажатие кнопок
            self.allowed = True
            self.how_many_times(True)
            self.save_picture()
            self.rdwindow = Rdimm()
            self.rdwindow.show()
            self.hide()
            self.show()

        # вызывается окно с историей изменений
        elif sender == 'История изменений' and self.allowed:

            self.story_img = Story_img()
            self.story_img.show()


        elif sender == 'Сохранить' and self.allowed:

            # для начала берём название будущего файла
            text, ok = QInputDialog.getText(self, 'Ввод', 'Название изображения')
            # название сразу корректируется под определенный формат
            name = f'{text}.jpg'
            # в диалоге выбирается директория, путь сохраняется в переменную
            dlg = QFileDialog.getExistingDirectory(self, "Выбрать папку")
            img = Image.open('rd_imm.jpg')
            img.save(f'{dlg}/{name}')

        elif sender == 'Рисование' and self.allowed:
            print('Автора настиг творческий кризис и дедлайн')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
