import pygame
import random
import sys
import sqlite3 as sl
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget


# Создаем наш класс
class Cubes(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('l1.ui', self)
        self.initUI()

    def initUI(self):
        # Прячем обьекты
        self.form.hide()
        self.close.hide()
        self.clear.hide()
        # Подключаем кнопки к функциям
        self.play.clicked.connect(self.game)
        self.games.clicked.connect(self.last_games)
        self.close.clicked.connect(self.last_games)
        self.clear.clicked.connect(self.deleter)
        # Задаем значения переменным
        self.scorebd = ''
        self.lvlbd = ''
        self.col_bonusbd = ''
        # Подключение бызы данных
        baza = sl.connect('l1.db')
        cur = baza.cursor()
        game = cur.execute("SELECT * FROM games ORDER BY id DESC")
        # Добавление даных из базы в выводной лист
        for row in game:
            self.form.addItems([row[0], row[1], row[2], ''])
        # Отключение от бызы данных
        baza.close()

    # Метод просмотра последних игр
    def last_games(self):
        # Если нажали последние игры
        if self.sender() == self.games:
            self.form.show()
            self.close.show()
            self.clear.show()
            self.play.hide()
            self.games.hide()
        # Иначе (если нажали закрыть)
        else:
            self.form.hide()
            self.close.hide()
            self.clear.hide()
            self.play.show()
            self.games.show()

    # Метод добавления объектов в базу данных
    def addbd(self):
        # Очищение выводного листа
        self.form.clear()
        # Подключение бызы данных
        baza = sl.connect('l1.db')
        cur = baza.cursor()
        # Добавление данных в базу
        cur.execute(f'INSERT INTO games (scorebd, lvlbd, col_bonusbd) values(?, ?, ?)',
                    (f'Счет: {self.scorebd}', f'Последняя волна: {self.lvlbd}',
                     f'Количество собраных бонусов: {self.col_bonusbd}'))
        # Сохранение изменений в базе
        baza.commit()
        # Условие
        game = cur.execute("SELECT * FROM games ORDER BY id DESC")
        # Добавление даных из базы в выводной лист
        for row in game:
            self.form.addItems([row[0], row[1], row[2], ''])
        # Отключение от бызы данных
        baza.close()

    # Метод удаления объектов из бызы данных
    def deleter(self):
        # Подключение бызы данных
        baza = sl.connect('l1.db')
        cur = baza.cursor()
        # Удаление данныз в базе
        cur.execute('DELETE from games')
        # Сохранение изменений в базе
        baza.commit()
        # Отключение от бызы данных
        baza.close()
        # Очищение выводного листа
        self.form.clear()
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cubes()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
