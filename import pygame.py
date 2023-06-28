import pygame
pygame.init()


screen_width = 1500

screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tax Buddy')

bg_img = pygame.image.load('img/t4_bg.png')
floor = pygame.image.load('img/floor.png')
start_button = pygame.image.load('img/start_button.png')
platform_14 = pygame.image.load('img/block_14.png')
platform = pygame.image.load('img/block.png')
platform_end = pygame.image.load('img/block_end.png')


run = True
while run:

    screen.blit(bg_img, (0,0))
    screen.blit(floor, (0,450))
    screen.blit(start_button, (35,225))
    screen.blit(platform_14, (500, 200))
    screen.blit(platform, (850, 150))
    screen.blit(platform_end, (1250, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()