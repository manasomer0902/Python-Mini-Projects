import pygame
pygame.init()

# creating a window

screen_height = 1200
screen_width = 800

screen = pygame.display.set_mode((screen_height, screen_width))
clock = pygame.time.Clock()


game_loop = False

while game_loop == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = True

    screen.fill('black')

    pygame.display.update()
    clock.tick(60)

pygame.quit()
