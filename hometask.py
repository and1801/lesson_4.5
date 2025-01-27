import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60

# Загрузка изображений
player_image = pygame.image.load('pngwing.png')
enemy_image = pygame.image.load('mush.png')

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game")

# Шрифт для отображения текста
font = pygame.font.SysFont(None, 48)


# Класс игрока
class Player:
    def __init__(self):
        self.rect = player_image.get_rect(center=(WIDTH / 2, HEIGHT - PLAYER_SIZE))
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())  # Ограничиваем движение экраном

    def draw(self):
        screen.blit(player_image, self.rect)


# Класс врага
class Enemy:
    def __init__(self):
        x = random.randint(0, WIDTH - ENEMY_SIZE)
        y = random.randint(0, HEIGHT - ENEMY_SIZE)
        self.rect = enemy_image.get_rect(topleft=(x, y))
        self.speed = random.randint(2, 4)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.change_direction_timer = random.randint(30, 90)

    def move(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction_y *= -1

        self.change_direction_timer -= 1
        if self.change_direction_timer <= 0:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
            self.change_direction_timer = random.randint(30, 90)

    def draw(self):
        screen.blit(enemy_image, self.rect)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def show_start_screen():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text("Survival Game", font, (255, 255, 255), screen, WIDTH / 4, HEIGHT / 3)
        draw_text("Press SPACE to Start", font, (255, 255, 255), screen, WIDTH / 4, HEIGHT / 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Начать игру


def show_game_over_screen(score):
    screen.fill(BACKGROUND_COLOR)
    draw_text(f"Game Over! Your score: {int(score)}", font, (255, 255, 255), screen, WIDTH / 4, HEIGHT / 3)
    pygame.display.flip()

    pygame.time.wait(2000)  # Задержка перед возвратом на стартовый экран
    return  # Возврат на стартовый экран для перезапуска


def game():
    while True:
        show_start_screen()

        player = Player()
        enemies = [Enemy() for _ in range(5)]
        score = 0  # Сброс счётчика перед каждой игрой
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            player.move(dx, dy)

            screen.fill(BACKGROUND_COLOR)
            player.draw()

            for enemy in enemies:
                enemy.move()
                enemy.draw()
                if player.rect.colliderect(enemy.rect):
                    show_game_over_screen(score)  # Показ экрана окончания игры
                    break  # Выход из цикла игры после показа экрана окончания
            else:
                # Отображение счёта, если нет столкновения
                score += 1 / FPS  # Увеличение счёта
                draw_text(f"Score: {int(score)}", font, (255, 255, 255), screen, 40, 10)
                pygame.display.flip()
                clock.tick(FPS)
                continue

            break  # Выход из основного игрового цикла при окончании игры


game()
