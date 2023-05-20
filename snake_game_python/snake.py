# -*- coding: utf-8 -*-

# подключение библиотек для игры
import pygame
import random
import time

# инициализация игры
pygame.init()

# параметры экрана
width = 800
height = 600

# создание окна с игрой
screen = pygame.display.set_mode((width, height))

# название окна с игрой
pygame.display.set_caption('Snake')

# добавление музыки в игру
pygame.mixer.music.load('melody.mp3')

# проигрывание музыки во время воспроизведения игры
pygame.mixer.music.play(-1)

# жёлтый цвет для экрана игры
yellow = (237, 255, 33)

# заполнение экрана игры жёлтым цветом
screen.fill(yellow)

# требуется для движения змейки
clock = pygame.time.Clock()

# основные координаты змейки
x = 400
y = 300

# изменение координатат змейки по осям x и y
x_change = 0
y_change = 0

# размер одного элемента игрового поля
snake_size = 10

# длина змейки
snake_length = 1

# тело змейки
snake_body = []

# скорость змейки
snake_speed = 2

# генерация еды для змейки по осям x и y
food_x = random.randint(20, 780)
food_y = random.randint(20, 580)

# размер еды для змейки
food_size = 10

class Game:

    # создание счётчика для считывания очков
    score = 0

    # функция, создающая змейку
    def snake(snake_size, snake_body):
        for x in snake_body:
            pygame.draw.rect(screen, (0, 0, 0), [x[0], x[1], snake_size, snake_size])

    # функция, создающая еду для змейки
    def food(surface, food_x, food_y, food_size):
        pygame.draw.rect(surface, (255, 0, 0), [food_x, food_y, food_size, food_size])

    # функция, которая следит и обновляет счётчик игрока
    def update_score(score):
        font = pygame.font.SysFont('comicsans', 30)
        score_label = font.render('Score: ' + str(score), True, (0, 0, 0))
        screen.blit(score_label, (620, 10))

    # работа игры
    game_over = False
    while not game_over:
        # при выходе змейки из границ игрового поля игра заканчивает свою работу
        if x >= width or x < 0 or y >= height or y < 0:
            # змейка по оси x может двигаться только в одном направлении (либо вправо, либо влево); змейка по оси y может двигаться только в одном направлении (либо вверх, либо вниз)
            if snake_head[0] > width - 10 or snake_head[0] < 0 or snake_head[1] > height - 10 or snake_head[1] < 0:
                game_over = True
                for x in snake_body[:-1]:
                    if x == snake_head:
                        game_over = True
        for i in snake_body[:-1]:
            # при столкновении змейки саму в себя, игра завершается
            if i[0] == snake_head[0] and i[1] == snake_head[1]:
                game_over = True

        # требуется для того, чтобы экран игры не закрывался при начале её работы
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()

            # изменение координат змейки по осям x и y при её движении в разные стороны
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_change = snake_speed
                    y_change = 0
                    # при поворатах змейки в разные стороны срабатывают звуковые эффекты
                    pygame.mixer.Sound('turn.wav').play()

                if event.key == pygame.K_LEFT:
                    x_change = -snake_speed
                    y_change = 0
                    # при поворатах змейки в разные стороны срабатывают звуковые эффекты
                    pygame.mixer.Sound('turn.wav').play()

                if event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -snake_speed
                    # при поворатах змейки в разные стороны срабатывают звуковые эффекты
                    pygame.mixer.Sound('turn.wav').play()

                if event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = snake_speed
                    # при поворатах змейки в разные стороны срабатывают звуковые эффекты
                    pygame.mixer.Sound('turn.wav').play()

        # обновление позиции змейки по осям x и y
        if x > width - 10:
            game_over = True
        if y > height - 10:
            game_over = True
        if x - 10 < 0:
            game_over = True
        if y - 10 < 0:
            game_over = True

        x += x_change
        y += y_change

        # голова змейки
        snake_head = []

        # реализация увеличения длины змейки через «вторую голову»
        snake_head.append(x)
        snake_head.append(y)
        snake_body.append(snake_head)
        if len(snake_body) > snake_length:
            del snake_body[0]

        # пересечение змейки с едой змейки
        if abs(x - food_x) < 10 and abs(y - food_y) < 10:

            # увеличение счётчика
            score += 1

            # увеличение скорости змейки
            snake_speed += 1

            # появление еды в произвольных местах на игровом поле
            food_x = random.randint(20, 780)
            food_y = random.randint(20, 580)

            # увеличение длины змейки
            snake_length += 1

            # при взятии еды срабатывает звуковой эффект
            pygame.mixer.Sound('eat.wav').play()

        # при поражении срабатывает звуковой эффект, а также воспроизводится вывод с итоговым результатом очков
        if game_over == True:
            score_font = pygame.font.SysFont('comicsans', 40)
            score_label = score_font.render('Your final score was: ' + str(score), True, (0, 0, 255))
            screen.blit(score_label, (250, 400))
            pygame.mixer.Sound('lose.wav').play()

        # заполнение экрана игры жёлтым цветом
        screen.fill(yellow)

        # вывод змейки
        snake(snake_size, snake_body)

        # вывод еды для змейки
        food(screen, food_x, food_y, food_size)

        # обновление счёта игрока
        update_score(score)

        # обновление экрана игры
        pygame.display.update()

        # частота кадров в секунду
        clock.tick(20)

class Text:

    # вывод сообщения о том, что игра завершена
    game_over_font = pygame.font.SysFont('comicsans', 60)
    game_over_label = game_over_font.render('Game Over!', True, (255, 0, 0))
    screen.blit(game_over_label, (300, 300))

    # вывод сообщения о счёте игрока
    score_font = pygame.font.SysFont('comicsans', 40)
    score_label = score_font.render('Your score was: ' + str(Game.score), True, (0, 0, 255))
    screen.blit(score_label, (250, 400))

# обновление экрана игры
pygame.display.update()

# ожидание трёх секунд после поражения, после чего окно игры закроется автоматически
time.sleep(3)

# завершение работы игры
pygame.quit()
quit()