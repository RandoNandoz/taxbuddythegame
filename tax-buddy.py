import pygame, sys


import random

import time

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()  # initiation pygame

pygame.display.set_caption("Tax Buddy")

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize the window


def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(" ".join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = " ".join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh


display = pygame.Surface((300, 200))

# class StaticEnemy(pygame.surface.Surface):


# class Enemy2(object):
#     def __init__(self, x, y):
#         self.original_x = x
#         self.original_y = y
#         self.x = x
#         self.y = y
#         self.width = 32
#         self.height = 32
#         self.walkRight = [pygame.image.load("sprites/po/running/running_1.png")]
#         self.walkLeft = [pygame.transform.flip(pygame.image.load("sprites/po/running/running_1.png"), True, False)]
#         self.movingRight = True
#     def move(self, scroll):
#         if self.movingRight:
#             self.x += 2
#             screen.blit(self.walkRight[0], (self.x - scroll[0], self.y - scroll[1]))
#             if self.x >= self.original_x + 64:
#                 self.movingRight = False
#         else:
#             self.x -= 2
#             screen.blit(self.walkRight[0], (self.x - scroll[0], self.y - scroll[1]))
#             if self.x <= self.original_x - 64:
#                 self.movingRight = True

# class Enemy(object):
#     def __init__(self, x, y, width, height, end):
#         self.walkRight = [pygame.image.load("sprites/po/running/running_1.png")]
#         self.walkLeft = [pygame.transform.flip(pygame.image.load("sprites/po/running/running_1.png"), True, False)]
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.end = end
#         self.path = [self.x, self.end]
#         self.walkCount = 0
#         self.vel = 3
#     def draw(self, window, A):
#         self.move()
#         if self.walkCount + 1 <= 33:
#             self.walkCount = 0
#         if self.vel > 0:
#             # window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
#             window.blit(self.walkRight[0],
#                         A
#                         )

#             self.walkCount += 1
#         else:
#             # window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
#             window.blit(self.walkLeft[0], A)
#             self.walkCount += 1
#     def move(self):
#         if self.vel > 0:
#             # going right
#             if self.x + self.vel < self.path[1]:
#                 self.x += self.vel
#             else:
#                 self.x *= -1
#                 self.walkCount = 0
#         else:
#             if self.x - self.vel > self.path[0]:
#                 self.x += self.vel
#             else:
#                 self.vel *= -1
#                 self.walkcount = 0
#         pass


global animation_frames
animation_frames = {}


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


tax_form_img = pygame.image.load("data/images/t4_form_1.png")
empty_tax_form_img = pygame.image.load("data/images/t1_form_empty.png")
i_love_canada = pygame.image.load("data/images/i_love_canada.png")
background_img = pygame.image.load("data/images/t4_bg.png")
start_menu_bg = pygame.image.load("data/images/start_menu_bg.png")
police_static = pygame.image.load("sprites/po/idle/idle_1.png")

win_img = pygame.image.load("data/images/win.png")

curr_sel = None

# class projectile()


def start_menu():
    black = (255, 255, 255)
    # start menu for the game, in pygame
    # start menu will have a start button, a quit button, and a settings button
    # start button will start the game
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # screen.fill((255, 255, 255))
        screen.blit(start_menu_bg, (0, 0))
        font = pygame.font.Font("pixelfont.ttf", 32)
        # TitleSurf, TitleRect = text_objects("Tax Buddy", font, black)
        StartText, StartRect = text_objects("Start", font, black)
        QuitText, QuitRect = text_objects("Quit", font, black)
        # TitleRect.center = ((WINDOW_SIZE[0] / 2), (WINDOW_SIZE[1] / 2))
        StartRect.center = ((WINDOW_SIZE[0] / 2), (WINDOW_SIZE[1] / 2))
        QuitRect.center = ((WINDOW_SIZE[0] / 2), (WINDOW_SIZE[1] / 2) + 50)

        mouse = pygame.mouse.get_pos()

        if StartRect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            return
        if QuitRect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            pygame.quit()
            quit()

        # screen.blit(TitleSurf, TitleRect)
        screen.blit(StartText, StartRect)
        screen.blit(QuitText, QuitRect)

        pygame.display.update()
        clock.tick(15)


enemies = []
monies = []
police_bullets = []


def playing():
    fire_music = pygame.mixer.music.load("data/audio/Menu_music.wav")
    pygame.mixer.music.play(loops=-1)
    animation_database = {}
    animation_database["run"] = load_animation(
        "sprites/bmo-animations/running", [7, 14, 7, 14]
    )
    animation_database["idle"] = load_animation(
        "sprites/bmo-animations/idle", [7, 7, 7, 7, 7]
    )
    tax_jokes = [
        "Why did the T4 slip bring a ladder to work? Because it wanted to climb the corporate tax ladder!",
        "Why did the T5 go to a comedy club? Because it wanted to invest in some laughter and get a “dividend” of smiles!",
        "Why did the T3 form become a stand-up comedian? Because it always had trust-worthy jokes and delivered them with great interest!",
        "The Canadian system is broken up into tax brackets, each one with its own tax rate. As your income increases, you gradually move through these tax brackets, meaning the CRA takes more money from you, the more money you make!",
        "Why did the chicken cross road? Because it didn't want to pay taxes!",
        "We all love the hit game, tax evasion simulator! However, we all know we all know the sequel to that game is prison simulator. We don’t want prison. But there is another way to dodge taxes with tax credits!"
        "$7000 for tuition? Too much! The T2202 provides the CRA with information about tuition that might give you some of your money back in the form of tax credits!",
        "PAY YOUR TAXES",
        "They can't collect legal taxes from illegal money",
        "in this world nothing can be said to be certain, except death and taxes.",
    ]

    player_action = "idle"
    player_frame = 0
    player_flip = False

    # player_image = pygame.image.load('sprites/ripoff-bmo1.png')
    player_rect = pygame.Rect(64, 50, 32 - 3, 32)
    moving_right = False
    moving_left = False

    # player_location = [50,50]
    player_y_momentum = 0
    air_timer = 0

    shooting_cooldown = 0

    true_scroll = [0, 0]
    # po2 = Enemy2(206, 160)
    joke_time = -1
    joke_choice = 0
    while True:
        display.fill((146, 244, 255))

        # screen.split

        true_scroll[0] += (player_rect.x - true_scroll[0] - 32) / 20
        true_scroll[1] += (player_rect.y - true_scroll[1] - 112) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        tile_rects = []
        y = 0
        polices_on_scr = []
        for row in game_map:
            x = 0
            for tile in row:
                if tile == "1":
                    display.blit(
                        block_image,
                        (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]),
                    )
                if tile == "2":
                    display.blit(
                        blockRed_image,
                        (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]),
                    )
                if tile != "0":
                    tile_rects.append(
                        pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
                if tile == "t":
                    display.blit(
                        tax_form_img,
                        (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]),
                    )
                if tile == "e":
                    display.blit(
                        empty_tax_form_img,
                        (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]),
                    )
                if tile == "c":
                    display.blit(
                        i_love_canada,
                        (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]),
                    )
                # po1.draw(screen, (po1.x - scroll[0], po1.y - scroll[1]))
                # print(f"po1x: {po1.x}, po1: {po1.y}")
                if tile == "p":
                    p_r = police_static.get_rect()
                    p_r.topleft = (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1])
                    polices_on_scr.append(p_r)
                    display.blit(
                        police_static,
                        (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]),
                    )

                x += 1
            y += 1

        # for p in polices_on_scr:
        #     # if we collide with p, we lose
        #     collide = pygame.Rect.colliderect(player_rect, p)
        #     if collide:
        #         print("LOSE")

        # screen.blit(player_image, player_location)

        player_movement = [0, 0]

        if moving_right:
            player_movement[0] += 2
        if moving_left:
            player_movement[0] -= 2
        player_movement[1] += player_y_momentum
        # clamping the y momentum
        player_y_momentum += 0.25
        if player_y_momentum > 3:
            player_y_momentum = 3

        if player_movement[0] > 0:
            player_action, player_frame = change_action(
                player_action, player_frame, "run"
            )
            player_flip = False
        if player_movement[0] == 0:
            player_action, player_frame = change_action(
                player_action, player_frame, "idle"
            )
        if player_movement[0] < 0:
            player_action, player_frame = change_action(
                player_action, player_frame, "run"
            )
            player_flip = True

        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions["bottom"]:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1
        if collisions["top"]:
            player_y_momentum = -player_y_momentum

        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_image = animation_frames[player_img_id]
        display.blit(
            pygame.transform.flip(player_image, player_flip, False),
            (player_rect.x - scroll[0], player_rect.y - scroll[1]),
        )

        # fin_rect = Rect(100, 100, 100, 100)
        # fin_surf = pygame.Surface((100, 100))
        # display.blit(fin_surf, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        for count, money in enumerate(monies):
            money[1].x += 3 * money[0]
            money[1].change_frame(1)
            money[1].display(display, scroll)
            # test = e.collision_test(money, [enemy[1] for enemy in enemies])
            # for hit in test:
            #     for count, enemy in enumerate(enemies):
            #         if hit == enemy[1]:
            #             enemies.pop(count)

        for event in pygame.event.get():
            print(event)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game_state = "start_menu"

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if air_timer < 7:
                        player_y_momentum = -7
                if event.key == K_SPACE:
                    if shooting_cooldown < 0:
                        shooting_cooldown = 5

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
        shooting_cooldown -= 1

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        # po2.move(true_scroll)
        # if player_rect.top >
        # screen.blit(taxRed_image, (135 - scroll[0], 100 - scroll[1]))
        print(f"x: {player_rect.topright}")
        if player_rect.topright[0] >= 1184:
            pygame.mixer_music.stop()
            break

        if joke_time < 0:
            joke_choice = random.randint(0, len(tax_jokes) - 1)
            joke_time = 500
        renderTextCenteredAt(
            tax_jokes[joke_choice],
            pygame.font.Font("pixelfont.ttf", 12),
            (255, 0, 0),
            200,
            0,
            screen,
            400,
        )
        joke_time -= 1
        pygame.display.update()
        clock.tick(60)


def end_menu():
    # timer = 50
    # while timer > 0:
    screen.blit(win_img, (0, 0))
    pygame.display.update()
    time.sleep(10)
    clock.tick(50)


def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split("/")[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_durations:
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"
        animation_image = pygame.image.load(img_loc)  # .convert()
        # animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


def load_map(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map("game_map.txt")

lvl_1 = load_map

block_image = pygame.image.load("blocks/block.png")
blockRed_image = pygame.image.load("blocks/block-red.png")
TILE_SIZE = block_image.get_width()


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
    return rect, collision_types


# test_rect = pygame.Rect(100,100,100,50)

game_state = "start_menu"
shooting_cooldown = -1
# screen.blit(background_img, (0,0))

while True:  # game loop
    if game_state == "start_menu":
        pygame.mixer.music.load("data/audio/Boss_music.wav")
        pygame.mixer.music.play(-1)
        start_menu()
        pygame.mixer.music.stop()
        game_state = "playing"

    if game_state == "playing":
        playing()
        game_state = "end_menu"

    if game_state == "end_menu":
        pygame.mixer.music.load("data/audio/Menu_music_2.wav")
        pygame.mixer.music.play(-1)
        end_menu()
        pygame.mixer.music.stop()
        # start_menu()
        game_state = "start_menu"
        # game_state = "playing"

    # start_menu()
