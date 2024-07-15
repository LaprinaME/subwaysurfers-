import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Surfer Game")

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)

# Игровые параметры
player_width = 70
player_height = 150
player_x = screen_width // 2 - player_width // 2
player_y = screen_height // 2 - player_height // 2
player_speed = 5

obstacle_width = 100
obstacle_height = 190
obstacle_speed = 5
obstacle_interval = 300
obstacles = []

# Параметры фона
background_speed_near = 5
background_speed_far = 2

# Слои фона (спрайты)
background_near_objects = [[random.randint(0, screen_width), random.randint(0, screen_height)] for _ in range(10)]
background_far_objects = [[random.randint(0, screen_width), random.randint(0, screen_height)] for _ in range(10)]

# Загрузка спрайтов
player_image = pygame.image.load('player_sprite.png')
player_image = pygame.transform.scale(player_image, (player_width, player_height))

obstacle_images = [
    pygame.image.load('obstacle_sprite.png'),
    pygame.image.load('obstacle_sprite1.png'),
    pygame.image.load('obstacle_sprite2.png'),
    pygame.image.load('obstacle_sprite3.png')
]

# Масштабирование спрайтов препятствий
for i in range(len(obstacle_images)):
    obstacle_images[i] = pygame.transform.scale(obstacle_images[i], (obstacle_width, obstacle_height))

# Загрузка фонового изображения для стартового меню
menu_background_image = pygame.image.load('menu_background.png')
menu_background_image = pygame.transform.scale(menu_background_image, (screen_width, screen_height))

# Загрузка изображений для кнопки "Старт" с уменьшенным размером
start_button_image = pygame.image.load('start_button.png')
start_button_width = 200  # Новая ширина кнопки
start_button_height = 80  # Новая высота кнопки
start_button_image = pygame.transform.scale(start_button_image, (start_button_width, start_button_height))
start_button_rect = start_button_image.get_rect()
start_button_rect.center = (screen_width // 2, screen_height // 2 + 100)

# Загрузка изображения для спрайта сбоку с настраиваемым размером
sidebar_sprite_image = pygame.image.load('sidebar_sprite.png')
sidebar_sprite_width = 250  # Новая ширина спрайта
sidebar_sprite_height = 600  # Новая высота спрайта
sidebar_sprite_image = pygame.transform.scale(sidebar_sprite_image, (sidebar_sprite_width, sidebar_sprite_height))
sidebar_sprite_rect = sidebar_sprite_image.get_rect()
sidebar_sprite_rect.midright = (screen_width, screen_height // 2)

# Загрузка изображения фона для игры
game_background_image = pygame.image.load('background_image.png')
game_background_image = pygame.transform.scale(game_background_image, (screen_width, screen_height))

# Загрузка изображений для меню проигрыша
game_over_background = pygame.image.load('game_over_background.png')
game_over_background = pygame.transform.scale(game_over_background, (screen_width, screen_height))

game_over_sprite = pygame.image.load('game_over_sprite.png')
game_over_sprite = pygame.transform.scale(game_over_sprite, (400, 500))
game_over_sprite_rect = game_over_sprite.get_rect()
game_over_sprite_rect.center = (screen_width // 2, screen_height // 2 - 50)

exit_button_image = pygame.image.load('exit_button.png')
exit_button_width = 200
exit_button_height = 80
exit_button_image = pygame.transform.scale(exit_button_image, (exit_button_width, exit_button_height))
exit_button_rect = exit_button_image.get_rect()
exit_button_rect.center = (screen_width // 2, screen_height // 2 + 100)

restart_button_image = pygame.image.load('restart_button.png')
restart_button_width = 200
restart_button_height = 80
restart_button_image = pygame.transform.scale(restart_button_image, (restart_button_width, restart_button_height))
restart_button_rect = restart_button_image.get_rect()
restart_button_rect.center = (screen_width // 2, screen_height // 2 + 200)

clock = pygame.time.Clock()

# Функция для отрисовки игрока
def draw_player(x, y):
    screen.blit(player_image, (x, y))

# Функция для отрисовки препятствий
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle_images[obstacle[2]], (obstacle[0], obstacle[1]))

# Функция для отрисовки фона в игре
def draw_game_background():
    screen.blit(game_background_image, (0, 0))
    draw_background_scenery()

# Функция для отрисовки заднего плана
def draw_background_scenery():
    for obj in background_far_objects:
        pygame.draw.circle(screen, black, obj, 10)
        obj[1] += background_speed_far
        if obj[1] > screen_height:
            obj[1] = 0
            obj[0] = random.randint(0, screen_width)

    for obj in background_near_objects:
        pygame.draw.circle(screen, black, obj, 10)
        obj[1] += background_speed_near
        if obj[1] > screen_height:
            obj[1] = 0
            obj[0] = random.randint(0, screen_width)

# Функция для отрисовки стартового меню
def draw_menu():
    screen.blit(menu_background_image, (0, 0))
    screen.blit(start_button_image, start_button_rect)

# Функция для отрисовки спрайта сбоку
def draw_sidebar_sprite():
    screen.blit(sidebar_sprite_image, sidebar_sprite_rect)

# Функция для отрисовки меню проигрыша
def draw_game_over_menu():
    screen.blit(game_over_background, (0, 0))
    screen.blit(game_over_sprite, game_over_sprite_rect)
    screen.blit(exit_button_image, exit_button_rect)
    screen.blit(restart_button_image, restart_button_rect)

# Основной игровой цикл
in_menu = True
in_game = False
game_over = False
running = True
while running:
    if in_menu:
        draw_menu()
        draw_sidebar_sprite()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    in_menu = False
                    in_game = True
                    # Сброс всех параметров для начала игры заново
                    player_x = screen_width // 2 - player_width // 2
                    player_y = screen_height // 2 - player_height // 2
                    obstacles = []
                    for i in range(len(background_near_objects)):
                        background_near_objects[i] = [random.randint(0, screen_width), random.randint(0, screen_height)]
                    for i in range(len(background_far_objects)):
                        background_far_objects[i] = [random.randint(0, screen_width), random.randint(0, screen_height)]

    elif in_game:
        draw_game_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            for obj in background_near_objects:
                obj[0] += background_speed_near
            for obj in background_far_objects:
                obj[0] += background_speed_far
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
            for obj in background_near_objects:
                obj[0] -= background_speed_near
            for obj in background_far_objects:
                obj[0] -= background_speed_far

        # Добавление новых препятствий
        if len(obstacles) == 0 or obstacles[-1][1] > obstacle_interval:
            obstacles.append([random.randint(0, screen_width - obstacle_width), -obstacle_height, random.randint(0, 3)])

        # Обновление координат препятствий
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed

        # Удаление препятствий, вышедших за пределы экрана
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < screen_height]

        # Проверка на столкновение игрока с препятствиями
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
            if player_rect.colliderect(obstacle_rect):
                in_game = False
                game_over = True
                break

        # Отрисовка игрока и препятствий
        draw_player(player_x, player_y)
        draw_obstacles(obstacles)

    elif game_over:
        draw_game_over_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif restart_button_rect.collidepoint(mouse_pos):
                    # Перезапуск игры по клику на кнопку рестарта
                    game_over = False
                    in_menu = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
