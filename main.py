#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from player import *
from blocks import *

# Объявляем переменные
WIN_WIDTH = 988  # Ширина создаваемого окна
WIN_HEIGHT = 598  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_IMAGE = pygame.image.load('background-color/background_color_1.jpg')


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def make_level():
    global level, platforms, entities, hero, hero_2
    entities = pygame.sprite.Group()
    entities.add(hero)
    entities.add(hero_2)
    platforms = []
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля


def main():
    global level, entities, platforms, hero, hero_2
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    clock = pygame.time.Clock()
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон

    hero_2 = Player(55, 514)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    hero = Player(835, 514)  # создаем героя по (x,y) координатам
    a = d = False  # по умолчанию - стоим
    w = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)
    entities.add(hero_2)

    level = [
        "-                                    -",
        "-                                    -",
        "-                                    -",
        "-                                    -",
        "-----                            -----",
        "---     *                    *     ---",
        "--    ---                    ---    --",
        "-      --                    --      -",
        "-       -                    -       -",
        "-       ---                ---       -",
        "--   -----                  -----   --",
        "-       -                    -       -",
        "-       *                    *       -",
        "-      --                    --      -",
        "---     -                    -     ---",
        "--      *                    *      --",
        "-     ----                  ----     -",
        "-        -                  -        -",
        "-----    *                  *    -----",
        "-       --                  --       -",
        "-                                    -",
        "-                                    -",
        "--------------------------------------",
        "--------------------------------------"]

    make_level()

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)
    running = True

    while running:  # Основной цикл программы
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if e.key == K_w:
                    w = True
                elif e.key == K_a:
                    a = True
                elif e.key == K_d:
                    d = True
                elif e.key == K_s:
                    new_l = list(map(list, level))
                    if new_l[hero_2.rect.y // 26 + 2][hero_2.rect.x // 26] == " ":
                        new_l[hero_2.rect.y // 26 + 2][hero_2.rect.x // 26] = "-"
                        level = list(map("".join, new_l))
                        make_level()
                elif e.key == K_UP:
                    up = True
                elif e.key == K_LEFT:
                    left = True
                elif e.key == K_RIGHT:
                    right = True
                elif e.key == K_DOWN:
                    new_l = list(map(list, level))
                    if new_l[hero.rect.y // 26 + 2][hero.rect.x // 26] == " ":
                        new_l[hero.rect.y // 26 + 2][hero.rect.x // 26] = "-"
                        level = list(map("".join, new_l))
                        make_level()

            elif e.type == KEYUP:
                if e.key == K_w:
                    w = False
                elif e.key == K_d:
                    d = False
                elif e.key == K_a:
                    a = False
                elif e.key == K_UP:
                    up = False
                elif e.key == K_RIGHT:
                    right = False
                elif e.key == K_LEFT:
                    left = False

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        hero.update(left, right, up, platforms)  # передвижение
        hero_2.update(a, d, w, platforms)  # передвижение
        entities.draw(screen)  # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран
        clock.tick(75)


if __name__ == "__main__":
    main()
