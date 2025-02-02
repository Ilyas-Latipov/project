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
        self.tipe_move = 0
        self.tipe_lvl = 0
        self.form.hide()
        self.close.hide()
        self.clear.hide()
        self.lvl_tipes = [self.lvl1, self.lvl2, self.lvl3, self.lvl4]
        for el in self.lvl_tipes:
            el.clicked.connect(self.tipes_move)
        for el in self.lvl_tipes:
            el.hide()
        self.move_tipes = [self.tipe1, self.tipe2, self.text_tipe1, self.text_tipe2]
        for el in self.move_tipes:
            el.hide()
        self.tipe1.clicked.connect(self.game)
        self.tipe2.clicked.connect(self.game)
        # Подключаем кнопки к функциям
        self.play.clicked.connect(self.lvls)
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
            self.slovo.hide()
        # Иначе (если нажали закрыть)
        else:
            self.form.hide()
            self.close.hide()
            self.clear.hide()
            self.play.show()
            self.games.show()
            self.slovo.show()
    # Метод выбора сложности
    def lvls(self):
        self.slovo.setText('Выберите уровень сложности:')
        self.play.hide()
        self.games.hide()
        for el in self.lvl_tipes:
            el.show()

    # Метод выбора типа управления
    def tipes_move(self):
        self.tipe_lvl = self.sender().text()
        self.slovo.setText('Выберите тип управления:')
        for el in self.lvl_tipes:
            el.hide()
        for el in self.move_tipes:
            el.show()


    # Метод добавления объектов в базу данных
    def addbd(self):
        # Очищение выводного листа
        self.form.clear()
        # Подключение бызы данных
        baza = sl.connect('l1.db')
        cur = baza.cursor()
        # Добавление данных в базу
        cur.execute(f'INSERT INTO games (scorebd, lvlbd, col_bonusbd, tipe_lvlbd) values(?, ?, ?, ?)',
                    (f'Счет: {int(self.score)}', f'Последняя волна: {self.lvl}',
                     f'Количество собраных бонусов: {self.col_bonus}', f'Сложность: {self.tipe_lvl[13:]}'))
        # Сохранение изменений в базе
        baza.commit()
        # Условие
        game = cur.execute("SELECT * FROM games ORDER BY id DESC")
        # Добавление даных из базы в выводной лист
        for row in game:
            self.form.addItems([row[0], row[1], row[2], row[3], ''])
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

    # Метод запуска самой игры на pygame
    def game(self):
        for el in self.move_tipes:
            el.hide()
        self.tipe_move = int(self.sender().text()[0])
        if __name__ == '__main__':
            pygame.init()
            # Название окна
            pygame.display.set_caption('Кубики')
            # Размеры окна
            SIZE = 800, 800
            self.sc = pygame.display.set_mode(SIZE)
            # Основные переменные
            self.new_start()
            # Пока не нажали крестик
            while not self.exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit = True
                # Если игра оконченна
                if self.game_over:
                    if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                        self.new_start()
                    # Один раз рисуем проигрыш и пояснение
                    if self.restart == 2:
                        font = pygame.font.SysFont('0', 60)
                        text = font.render(f'Игра окончена! Ваш счет: {int(self.score)}', True, 'white')
                        self.sc.blit(text, (400 - text.get_width() // 2, 400))
                        font = pygame.font.SysFont('0', 40)
                        text = font.render(f'Чтобы перезапустить нажмите - Backspace', True, 'white')
                        self.sc.blit(text, (400 - text.get_width() // 2, 500))
                        self.restart = -2
                        self.addbd()
                    # Один раз рисуем паузу и пояснение
                    elif self.restart == 0:
                        font = pygame.font.SysFont('0', 200)
                        text = font.render(f'Пауза', True, 'white')
                        self.sc.blit(text, (400 - text.get_width() // 2, 300))
                        font = pygame.font.SysFont('0', 40)
                        text = font.render(f'Чтобы продолжить нажмите - Tab', True, 'white')
                        self.sc.blit(text, (400 - text.get_width() // 2, 500))
                        text = font.render(f'Чтобы перезапустить нажмите - Backspace', True, 'white')
                        self.sc.blit(text, (400 - text.get_width() // 2, 600))
                        self.restart = -1
                        self.addbd()
                    # Вызов метода всегда кроме проигрыша
                    if self.restart != -2:
                        self.pause()
                # Иначе (если игра не оконченна)
                else:
                    self.pause()
                    self.move()
                    self.sc.fill((self.hard, 0, 0))
                    self.dead = 0
                    # Повторяется один раз когда все кубики вышли за границы окна
                    if self.restart == 1:
                        self.new()
                    # Отрисовка щита (Эфект)
                    if self.protect == 1:
                        pygame.draw.rect(self.sc, (0, 255, 255), (self.x_pospl, self.y_pospl, 20, 20))
                    # Отрисовка кубика игрока
                    pygame.draw.rect(self.sc, 'white', (self.x_pospl, self.y_pospl, 20, 20), 2)
                    self.move_cubes_red()
                    self.move_cubes_green()
                    if self.lvl % 2 == 0:
                        self.bonusdef()
                    # Вывод данных игрока
                    font = pygame.font.SysFont('0', 30)
                    text = font.render(f'Счет: {int(self.score)} |', True, 'white')
                    self.sc.blit(text, (0, 0))
                    text = font.render(f'Волна: {self.lvl} |', True, 'white')
                    self.sc.blit(text, (145, 0))
                    text = font.render(f'Собрано бонусов: {self.col_bonus} |', True, 'white')
                    self.sc.blit(text, (270, 0))
                    text = font.render(f'Бонус: {self.last_bonus}', True, 'white')
                    self.sc.blit(text, (507, 0))
                    if self.restart == 0:
                        self.new_cubes()
                    # Очки всегда немного прибавляются
                    self.score += 0.017
                # Задержка
                self.clock.tick(self.FPS)
                # Обновление экрана
                pygame.display.flip()
            # Выход
            pygame.quit()
            self.slovo.setText('И снова привет! ;)')
            self.play.show()
            self.games.show()
            # Вызов метода записи данных в базу данных
            self.addbd()

    # Метод движения игрока
    def move(self):
        # Тип управления буквами
        if self.tipe_move == 1:
            if pygame.key.get_pressed()[pygame.K_w]:
                # Если мы идем по диагонали скорость будет неполной так как она еще будет дополняться -
                # другой стрелкой управления
                if not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_a]:
                    if self.y_pospl - self.speed / 2 >= 0:
                        self.y_pospl -= self.speed / 2
                if self.y_pospl - self.speed / 2 >= 0:
                    self.y_pospl -= self.speed / 2
            if pygame.key.get_pressed()[pygame.K_s]:
                if not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_a]:
                    if self.y_pospl + self.speed / 2 <= 780:
                        self.y_pospl += self.speed / 2
                if self.y_pospl + self.speed / 2 <= 780:
                    self.y_pospl += self.speed / 2
            if pygame.key.get_pressed()[pygame.K_a]:
                if not pygame.key.get_pressed()[pygame.K_w] and not pygame.key.get_pressed()[pygame.K_s]:
                    if self.x_pospl - self.speed / 2 >= 0:
                        self.x_pospl -= self.speed / 2
                if self.x_pospl - self.speed / 2 >= 0:
                    self.x_pospl -= self.speed / 2
            if pygame.key.get_pressed()[pygame.K_d]:
                if not pygame.key.get_pressed()[pygame.K_w] and not pygame.key.get_pressed()[pygame.K_s]:
                    if self.x_pospl + self.speed / 2 <= 780:
                        self.x_pospl += self.speed / 2
                if self.x_pospl + self.speed / 2 <= 780:
                    self.x_pospl += self.speed / 2
        # Тип управления стрелками
        else:
            if pygame.key.get_pressed()[pygame.K_UP]:
                # Если мы идем по диагонали скорость будет неполной так как она еще будет дополняться -
                # другой стрелкой управления
                if not pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.key.get_pressed()[pygame.K_LEFT]:
                    if self.y_pospl - self.speed / 2 >= 0:
                        self.y_pospl -= self.speed / 2
                if self.y_pospl - self.speed / 2 >= 0:
                    self.y_pospl -= self.speed / 2
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if not pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.key.get_pressed()[pygame.K_LEFT]:
                    if self.y_pospl + self.speed / 2 <= 780:
                        self.y_pospl += self.speed / 2
                if self.y_pospl + self.speed / 2 <= 780:
                    self.y_pospl += self.speed / 2
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]:
                    if self.x_pospl - self.speed / 2 >= 0:
                        self.x_pospl -= self.speed / 2
                if self.x_pospl - self.speed / 2 >= 0:
                    self.x_pospl -= self.speed / 2
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]:
                    if self.x_pospl + self.speed / 2 <= 780:
                        self.x_pospl += self.speed / 2
                if self.x_pospl + self.speed / 2 <= 780:
                    self.x_pospl += self.speed / 2

    # Метод паузы
    def pause(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and not self.game_over:
            self.game_over = True
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.game_over = False
            self.restart = 0

    # Метод обновления кубиков
    def new(self):
        # Повторяется один раз когда все кубики вышли за границы окна
        if self.lvl <= 50:
            if self.hard + 4 <= 200:
                self.hard += 4
        else:
            if self.hard + 2.25 <= 245:
                self.hard += 2.25
        if self.lvl % 51 == 0:
            self.score += 50000
        # Обновление списков координат и не только
        self.x_posleftred = []
        self.y_posleftred = []
        self.x_posupred = []
        self.y_posupred = []
        self.x_posrightred = []
        self.y_posrightred = []
        self.x_posdownred = []
        self.y_posdownred = []
        self.x_posgreen = []
        self.y_posgreen = []
        self.green_nap = []
        self.bonus_cords = []
        # Появления кубика бонуса на каждой второй волне
        if self.lvl % 2 == 0:
            # Рандомные координаты бонус кубика по осям Х и У
            for i in range(2):
                self.bonus_cords.append(random.randint(20, 780))
            # Рандомный бонус (его числовой порядок)
            self.bonus = random.randint(1, 4)
        # Добовление в списки рандомных координат красных кубиков по осям Х и У
        for i in range(int(self.tipe_lvl[:2]) // 4):
            self.x_posleftred.append(random.randint(-780, -20))
            self.y_posleftred.append(random.randint(20, 780))
            self.x_posupred.append(random.randint(20, 780))
            self.y_posupred.append(random.randint(-780, -20))
            self.x_posrightred.append(random.randint(820, 1780))
            self.y_posrightred.append(random.randint(20, 780))
            self.x_posdownred.append(random.randint(20, 780))
            self.y_posdownred.append(random.randint(820, 1780))
        # Рандомное количество зеленых кубиков
        self.col_green = random.randint(1, 4)
        # Добовление в списки рандомных координат зеленых кубиков по осям Х и У
        for i in range(self.col_green):
            self.x_posgreen.append(random.randint(100, 700))
            self.y_posgreen.append(random.randint(100, 700))
            # Рандомное направление зеленых кубиков (числовой порядок направления)
            self.green_nap.append(random.randint(1, 4))
        # Чтобы не повторялось
        self.restart = 0

    # Метод движения и проверки столкновения красных кубиков
    def move_cubes_red(self):
        for i in range(int(self.tipe_lvl[:2]) // 4):
            # Передвижение красных кубиков по окну
            self.x_posleftred[i] += self.v_red / self.FPS
            self.y_posupred[i] += self.v_red / self.FPS
            self.x_posrightred[i] -= self.v_red / self.FPS
            self.y_posdownred[i] -= self.v_red / self.FPS
            pygame.draw.rect(self.sc, 'red', (int(self.x_posleftred[i]), int(self.y_posleftred[i]), 20, 20))
            pygame.draw.rect(self.sc, 'red', (int(self.x_posupred[i]), int(self.y_posupred[i]), 20, 20))
            pygame.draw.rect(self.sc, 'red', (int(self.x_posrightred[i]), int(self.y_posrightred[i]), 20, 20))
            pygame.draw.rect(self.sc, 'red', (int(self.x_posdownred[i]), int(self.y_posdownred[i]), 20, 20))
            if ((int(self.x_posleftred[i]) - 10 <= self.x_pospl - 10 <= int(self.x_posleftred[i]) + 10 or \
                 int(self.x_posleftred[i]) - 10 <= self.x_pospl + 10 <= int(self.x_posleftred[i]) + 10) and \
                    (int(self.y_posleftred[i]) - 10 <= self.y_pospl - 10 <= int(self.y_posleftred[i]) + 10 or \
                     int(self.y_posleftred[i]) - 10 <= self.y_pospl + 10 <= int(self.y_posleftred[i]) + 10)):
                # При касании игра останавливается
                if self.protect != 1:
                    self.game_over = True
                    # Эфекты касания
                    pygame.draw.rect(self.sc, 'red', (self.x_pospl + 1, self.y_pospl + 1, 18, 18))
                    self.restart = 2
                # Щит спасает от касания и обнуляется
                else:
                    self.bonus = 0
                    self.protect = 0
                    # Перемещения красного кубика за карту чтобы вы его опять не коснулись
                    self.x_posleftred[i] = 820
                    self.y_posleftred[i] = 820
            elif ((int(self.x_posupred[i]) - 10 <= self.x_pospl - 10 <= int(self.x_posupred[i]) + 10 or \
                   int(self.x_posupred[i]) - 10 <= self.x_pospl + 10 <= int(self.x_posupred[i]) + 10) and \
                  (int(self.y_posupred[i]) - 10 <= self.y_pospl - 10 <= int(self.y_posupred[i]) + 10 or \
                   int(self.y_posupred[i]) - 10 <= self.y_pospl + 10 <= int(self.y_posupred[i]) + 10)):
                if self.protect != 1:
                    self.game_over = True
                    pygame.draw.rect(self.sc, 'red', (self.x_pospl + 1, self.y_pospl + 1, 18, 18))
                    self.restart = 2
                else:
                    self.bonus = 0
                    self.protect = 0
                    self.x_posupred[i] = 820
                    self.y_posupred[i] = 820
            elif (int(self.x_posrightred[i]) - 10 <= self.x_pospl - 10 <= int(self.x_posrightred[i]) + 10 or \
                  int(self.x_posrightred[i]) - 10 <= self.x_pospl + 10 <= int(self.x_posrightred[i]) + 10) and \
                    (int(self.y_posrightred[i]) - 10 <= self.y_pospl - 10 <= int(self.y_posrightred[i]) + 10 or \
                     int(self.y_posrightred[i]) - 10 <= self.y_pospl + 10 <= int(self.y_posrightred[i]) + 10):
                if self.protect != 1:
                    self.game_over = True
                    pygame.draw.rect(self.sc, 'red', (self.x_pospl + 1, self.y_pospl + 1, 18, 18))
                    self.restart = 2
                else:
                    self.bonus = 0
                    self.protect = 0
                    self.x_posrightred[i] = 820
                    self.y_posrightred[i] = 820
            elif ((int(self.x_posdownred[i]) - 10 <= self.x_pospl - 10 <= int(self.x_posdownred[i]) + 10 or
                   int(self.x_posdownred[i]) - 10 <= self.x_pospl + 10 <= int(self.x_posdownred[i]) + 10) and
                  (int(self.y_posdownred[i]) - 10 <= self.y_pospl - 10 <= int(self.y_posdownred[i]) + 10 or
                   int(self.y_posdownred[i]) - 10 <= self.y_pospl + 10 <= int(self.y_posdownred[i]) + 10)):
                if self.protect != 1:
                    self.game_over = True
                    pygame.draw.rect(self.sc, 'red', (self.x_pospl + 1, self.y_pospl + 1, 18, 18))
                    self.restart = 2
                else:
                    self.bonus = 0
                    self.protect = 0
                    self.x_posdownred[i] = 820
                    self.y_posdownred[i] = 820

    # Метод движения и проверки столкновения зеленых кубиков
    def move_cubes_green(self):
        for i in range(self.col_green):
            # Определения направления движения и передвижение зеленых кубиков по окну
            if self.green_nap[i] == 1:
                self.x_posgreen[i] += self.v_green / self.FPS
            elif self.green_nap[i] == 2:
                self.x_posgreen[i] -= self.v_green / self.FPS
            elif self.green_nap[i] == 3:
                self.y_posgreen[i] += self.v_green / self.FPS
            elif self.green_nap[i] == 4:
                self.y_posgreen[i] -= self.v_green / self.FPS
            pygame.draw.rect(self.sc, 'green', (int(self.x_posgreen[i]), int(self.y_posgreen[i]), 20, 20))
            # Проверка коснулся ли игрок зеленого кубика
            if ((int(self.x_posgreen[i]) - 10 <= self.x_pospl - 10 <= int(self.x_posgreen[i]) + 10 or
                int(self.x_posgreen[i]) - 10 <= self.x_pospl + 10 <= int(self.x_posgreen[i]) + 10) and
                (int(self.y_posgreen[i]) - 10 <= self.y_pospl - 10 <= int(self.y_posgreen[i]) + 10 or
                 int(self.y_posgreen[i]) - 10 <= self.y_pospl + 10 <= int(self.y_posgreen[i]) + 10)):
                # Эфекты касания
                pygame.draw.rect(self.sc, 'white',
                                 (int(self.x_posgreen[i]), int(self.y_posgreen[i]), 20, 20))
                pygame.draw.rect(self.sc, 'green', (self.x_pospl + 1, self.y_pospl + 1, 18, 18))
                # Перемещение кубиков зв карту
                self.x_posgreen[i] = 820
                self.y_posgreen[i] = 820
                # Прибавление очков
                self.score += 100

    # Метод бонусов
    def bonusdef(self):
        pygame.draw.rect(self.sc, 'blue', (self.bonus_cords[0], self.bonus_cords[1], 20, 20))
        # Проверка коснулся ли игрок кубика бонуса (синего)
        if (self.bonus_cords[0] - 10 <= self.x_pospl - 10 <= self.bonus_cords[0] + 10 or
            self.bonus_cords[0] - 10 <= self.x_pospl + 10 <= self.bonus_cords[0] + 10) and (self.bonus_cords[1] - 10
            <= self.y_pospl - 10 <= self.bonus_cords[1] + 10 or self.bonus_cords[1] - 10 <= self.y_pospl + 10 <=
            self.bonus_cords[1] + 10):
            # Эфекты касания
            pygame.draw.rect(self.sc, 'white', (self.bonus_cords[0], self.bonus_cords[1], 20, 20))
            pygame.draw.rect(self.sc, 'blue', (self.x_pospl + 1, self.y_pospl + 1, 18, 18))
            # Перемещение кубика за карту
            self.bonus_cords[0] = 820
            self.bonus_cords[1] = 820
            # Защитывание пойманого бонуса
            self.col_bonus += 1
            # Прибавление очков
            self.score += 50
            # Определение бонуса, его выполнение и защитывание его как последний подобранный
            if self.bonus == 1:
                self.protect = 1
                self.last_bonus = 'щит'
            if self.bonus == 2:
                self.speed += 0.2
                self.last_bonus = '+ваша скорость'
            if self.bonus == 3:
                self.last_bonus = '-скорость красных'
                if self.v_red - 20 >= 40:
                    self.v_red -= 20
            if self.bonus == 4:
                self.last_bonus = '-скорость зеленых'
                if self.v_green - 20 >= 10:
                    self.v_green -= 20

    # Метод проверки ушли ли все красные кубики за границу
    def new_cubes(self):
        # Проверка все ли кубики за картой
        for i in range(int(self.tipe_lvl[:2]) // 4):
            if self.x_posleftred[i] < 820:
                self.dead = 1
            if self.x_posrightred[i] > -20:
                self.dead = 1
            if self.y_posupred[i] < 820:
                self.dead = 1
            if self.y_posdownred[i] > -20:
                self.dead = 1
        # Если да то игра усложняется и кубики обновляются
        if self.dead == 0:
            self.col_green = 0
            self.restart = 1
            self.score += 50
            self.v_red += 5
            self.v_green += 5
            self.lvl += 1

    # Метод рестарта всей игры
    def new_start(self):
        self.exit = False
        self.game_over = False
        self.col_green = 0
        self.x_pospl = 400
        self.y_pospl = 400
        self.score = 0
        self.lvl = 1
        self.protect = 0
        self.col_bonus = 0
        self.last_bonus = 'не собран'
        self.bonus = 0
        self.speed = 1.5
        self.v_red = 80
        self.v_green = 35
        self.hard = 0
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.restart = 1

# Понятный вывод ошибок
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cubes()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())