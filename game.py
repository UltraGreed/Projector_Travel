import pygame
import random

from pygame.locals import *

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

is_next_move_left = True
boss_image = 'images/KIMOBO$$.png'
bullet_images = ['images/projector.png', 'images/bullet2.png']
vs_boss_bullet = 'images/projector.png'
enemy_images = ['images/Vano_enemy.png', 'images/Glina_enemy.png', 'images/Lesha_enemy.png',
                'images/Slava_enemy.png']
background_images = {'images/LICEY1.png', 'images/LICEY2.png', 'images/LICEY3.png'}
boss_fight_background = 'images/boss_back.png'
death_screen = 'images/Lose_back.png'
boss_bullet = 'images/xiaomi.png'
menu_image = 'images/main_licey.png'

# Загрузка звуков
start_sound = pygame.mixer.Sound('music/Introduction.wav')
start_sound.set_volume(1.5)
soundtrack = pygame.mixer.Sound('music/soundtrack.wav')
soundtrack.set_volume(0.125)
shoot_sound = pygame.mixer.Sound('music/shoot.wav')
shoot_sound.set_volume(0.6)
hit_sound = pygame.mixer.Sound('music/What_is_wrong_with_proector.wav')
death_sound = pygame.mixer.Sound('music/Very_sad.wav')

boss_res = (120, 172)
player_res = (93, 60)
enemy_res = (60, 93)
bullet_res = (15, 48)
vs_boss_bullet_res = (15, 48)
boss_bullet_res = (21, 44)

difficult = 1
back = 0
new_level = True
score = 0  # В начало
green = (0, 255, 0)
red = (255, 0, 0)
score_font = pygame.font.SysFont(None, 75)
score_text = 'SCORE:'
hp_text = 'ВВП'
hp_font = pygame.font.SysFont(None, 75)
death_text = 'R ЧТОБЫ ПОКАРАТЬ, ESC ВЫКЛЮЧИТЬ ПРОЕКТОР'
death_font = pygame.font.SysFont(None, 50)
name_font = pygame.font.SysFont(None, 150)
name_text = 'PROEKTOR TRAVEL'
button_text = 'НАЧАТЬ ИГРУ'
button_font = pygame.font.SysFont(None, 40)


def create_enemy(line, n):
    y = 100 * line
    x = 100 * n
    enemies[line].append(Enemy((x, y), random.choice(enemy_images), enemy_res))


def collision(rect1, rect2):
    return rect1.colliderect(rect2)


def shoot(pos, res, is_friendly):
    if is_friendly and is_boss_fight:
        friendly_bullets.append(FriendlyBullet((pos[0] + res[0] // 2, pos[1] + res[1] // 2 - 90),
                                               vs_boss_bullet))
        shoot_sound.play()
    elif is_friendly:
        friendly_bullets.append(FriendlyBullet((pos[0] + res[0] // 2, pos[1] + res[1] // 2 - 90),
                                               bullet_images[0]))
        shoot_sound.play()
    elif not is_friendly and is_boss_fight:
        enemy_bullets.append(EnemyBullet((pos[0] + res[0] // 2, pos[1] + res[1] // 2),
                                         boss_bullet))
    else:
        enemy_bullets.append(EnemyBullet((pos[0] + res[0] // 2, pos[1] + res[1] // 2),
                                         bullet_images[1]))


class Thing:
    def __init__(self, pos, image, res):
        self.resolution = res
        self.position = pos  # (X, Y)
        self.image = pygame.image.load(image).convert()
        self.image_surf = self.image
        self.image_surf.set_colorkey((0, 0, 0))

    def draw(self):
        self.image_rect = self.image_surf.get_rect(
            bottomright=(self.position[0] + self.resolution[0],
                         self.position[1] + self.resolution[1]))
        window.blit(self.image_surf, self.image_rect)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.resolution[0],
                           self.resolution[1])

    def move(self, x, y):  # X, y - перемещение по x и y
        self.position = (self.position[0] + x, self.position[1] + y)


class FriendlyBullet(Thing):
    def __init__(self, pos, image):
        if not is_boss_fight:
            super().__init__(pos, image, bullet_res)
        else:
            super().__init__(pos, image, vs_boss_bullet_res)

    def move(self, x, y):  # X, y - перемещение по x и y
        if self.get_y() < -50:
            friendly_bullets.pop(0)
        else:
            super().move(x, y)


class EnemyBullet(Thing):
    def __init__(self, pos, image):
        if is_boss_fight:
            super().__init__(pos, image, boss_bullet_res)
        else:
            super().__init__(pos, image, bullet_res)

    def move(self, x, y):  # X, y - перемещение по x и y
        if self.get_y() > 1100:
            enemy_bullets.pop(0)
        else:
            super().move(x, y)


class Enemy(Thing):
    pass


class Player(Thing):
    def __init__(self, pos, image, res, health):
        self.health = health
        super().__init__(pos, image, res)

    def dmg(self, n):
        self.health -= n

    def get_health(self):
        return self.health


class Boss(Player):
    def draw(self):
        self.image_surf = pygame.transform.rotate(self.image, 0)  # Image_name.png
        self.image_surf.set_colorkey((0, 0, 0))
        super().draw()


class Background(Thing):
    def __init__(self, pos, image, res):
        self.resolution = res
        self.position = pos  # (X, Y)
        self.image = pygame.image.load(image).convert()
        self.image_surf = self.image


enemies = [[], [], [], []]
friendly_bullets = list()
enemy_bullets = list()
bosses = []
delay = 10
x = delay
angle = 0
blue = 0, 191, 255
resolution = 1920, 1080
fullscreen = True
working = True
is_boss_fight = False

window: pygame.Surface = pygame.display.set_mode(resolution, FULLSCREEN)
pygame.display.set_caption('Proektor Travel')
menu = True
menu_image = Background((0, 0), menu_image, (1920, 1080))
while menu:
    menu_image.draw()
    pygame.draw.rect(window, red, pygame.Rect(900, 200, 200, 50))
    name_image = name_font.render(name_text, 10, red)
    button_image = button_font.render(button_text, 10, (255, 255, 255))
    window.blit(name_image, (400, 50))
    window.blit(button_image, (900, 210))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            working = False
            menu = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if collision(pygame.Rect(900, 200, 200, 50), pygame.Rect(*pos, 10, 10)):
                menu = False
        if event.type == KEYDOWN:
            if event.key == K_F1:
                if fullscreen:
                    window: pygame.Surface = pygame.display.set_mode(resolution)
                    fullscreen = False
                else:
                    window: pygame.Surface = pygame.display.set_mode(resolution, FULLSCREEN)
                    fullscreen = True
            if event.key == K_ESCAPE:
                working = False
                menu = False
            if event.key == K_KP_ENTER:
                menu = False

is_first_iteration = True
player = Player([800, 700], 'images/VVplayer.png', player_res, 3)
death_screen = Background((0, 0), death_screen, (1920, 1080))
did_death_happen = False
while working:
    if is_first_iteration:
        start_sound.play()
        pygame.time.delay(5200)
        soundtrack.play()
    # Обработка нажатий
    for event in pygame.event.get():
        if event.type == QUIT:
            working = False
        if event.type == KEYDOWN:
            if event.key == K_F1:
                if fullscreen:
                    window: pygame.Surface = pygame.display.set_mode(resolution)
                    fullscreen = False
                else:
                    window: pygame.Surface = pygame.display.set_mode(resolution,
                                                                     FULLSCREEN)
                    fullscreen = True
            if event.key == K_ESCAPE:
                working = False
            if event.key == K_SPACE and x == delay:
                shoot(player.position, player.resolution, True)
                x = 0
            if event.key == K_f:
                player.dmg(-100000)
            if event.key == K_g:
                enemies = [[], [], [], []]
                enemy_bullets = list()
                if is_boss_fight:
                    for boss in bosses:
                        boss.health = 0
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        if not player.get_x() - 10 <= 0:
            player.move(-20, 0)
    if keys[K_d]:
        if not player.get_x() + player.resolution[0] + 10 >= 1920:
            player.move(20, 0)
    if keys[K_w]:
        if not player.get_y() - 5 <= 700:
            player.move(0, -15)
    if keys[K_s]:
        if not player.get_y() + player.resolution[1] + 5 >= 1080:
            player.move(0, 15)

    # Работа с фонами и этапами
    if not any(enemies) and not is_boss_fight:
        if back == 9:
            if difficult < 4:
                for i in range(difficult):
                    bosses.append(Boss([800 + random.randint(-400, 400), 50], boss_image,
                                       boss_res, 2 + difficult))
            else:
                for i in range(4):
                    bosses.append(Boss([800 + random.randint(-400, 400), 50], boss_image,
                                       boss_res, 2 + difficult))
            is_boss_fight = True
            background = Background((0, 0), boss_fight_background, (1920, 1080))
        else:
            if back % 3 == 0 and background_images:
                background = Background((0, 0), background_images.pop(), (1920, 1080))
            if difficult < 4:
                for i in range(difficult):
                    for j in range(random.randint(1, 9)):
                        create_enemy(i, j)
            else:
                for i in range(4):
                    for j in range(random.randint(1, 12)):
                        create_enemy(i, j)
        back += 1
    if not working:
        break

    # Начинается отрисовка
    background.draw()

    for i in friendly_bullets:
        i.draw()
        for j in enemies.copy():
            for enemy in j:
                if collision(i.get_rect(), enemy.get_rect()):
                    j.remove(enemy)
                    if i in friendly_bullets:
                        friendly_bullets.remove(i)
                    score += 10
        if is_boss_fight:
            for boss in bosses:
                if collision(i.get_rect(), boss.get_rect()):
                    boss.dmg(1)
                    if i in friendly_bullets:
                        friendly_bullets.remove(i)
        i.move(0, -25)

    for i in enemy_bullets:
        i.draw()
        if collision(i.get_rect(), player.get_rect()):
            player.dmg(1)
            enemy_bullets.remove(i)
            if player.get_health():
                hit_sound.play()
        i.move(0, 5)

    for i in enemies:
        for j in i:
            j.draw()
            if random.randint(0, 100) == 100:
                shoot(j.position, j.resolution, False)
    if is_boss_fight:
        for boss in bosses:
            boss.draw()
            if is_next_move_left:
                if boss.get_x() - 10 >= 0:
                    boss.move(-10, 0)
                else:
                    is_next_move_left = False
            else:
                if boss.get_x() + 130 <= resolution[0]:
                    boss.move(10, 0)
                else:
                    is_next_move_left = True
            if random.randint(0, 7 + difficult) == 0:
                shoot((boss.position[0] + random.randint(-100, 100),
                       boss.position[1]), boss.resolution, False)
    player.draw()

    if any(enemies):
        for i in enemies:
            if is_next_move_left:
                if all(list(_[0].get_x() - 10 >= 0 for _ in
                            list(filter(lambda o: o, enemies)))):
                    for enemy in i:
                        enemy.move(-10, 0)
                else:
                    is_next_move_left = False
            else:
                if all(list(_[-1].get_x() + 70 <= resolution[0] for _
                            in list(filter(lambda o: o, enemies)))):
                    for enemy in i:
                        enemy.move(10, 0)
                else:
                    is_next_move_left = True

    if x < delay:
        x += 1

    while player.get_health() <= 0:
        if not did_death_happen:
            did_death_happen = True
            death_sound.play()
        soundtrack.stop()
        back = 0
        death_screen.draw()
        death_image = death_font.render(death_text, 0, (128, 0, 128))
        window.blit(death_image, (200, 450))
        score_image = score_font.render(score_text + str(score), 0, (128, 0, 128))
        window.blit(score_image, (200, 500))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                working = False
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    if fullscreen:
                        window: pygame.Surface = pygame.display.set_mode(resolution)
                        fullscreen = False
                    else:
                        window: pygame.Surface = pygame.display.set_mode(resolution,
                                                                         FULLSCREEN)
                        fullscreen = True
                if event.key == K_ESCAPE:
                    working = False
                    player.dmg(-1)
                if event.key == K_r:
                    player.dmg(-3)
                    back = 0
                    score = 0
                    friendly_bullets.clear()
                    enemy_bullets.clear()
                    enemies = [[], [], [], []]
                    background_images = {'images/LICEY1.png', 'images/LICEY2.png',
                                         'images/LICEY3.png'}
                    soundtrack.play(-1)
                    bosses.clear()
                    is_boss_fight = False
                    did_death_happen = False

    if is_boss_fight:
        for boss in bosses:
            if boss.get_health() == 0:
                bosses.remove(boss)
        if not bosses:
            difficult += 1
            is_boss_fight = False
            back = 0
            friendly_bullets.clear()
            enemy_bullets.clear()
            enemies = [[], [], [], []]
            score += 200
            player.dmg(-1)
            background_images = {'images/LICEY1.png', 'images/LICEY2.png',
                                 'images/LICEY3.png'}

    score_image = score_font.render(score_text + str(score), 0, red)
    health_text = hp_text[:player.get_health()]
    hp_image = hp_font.render(health_text, 0, red)
    window.blit(score_image, (75, 980))
    window.blit(hp_image, (1720, 980))
    is_first_iteration = False
    pygame.display.flip()
    pygame.time.Clock().tick(120)

pygame.quit()
