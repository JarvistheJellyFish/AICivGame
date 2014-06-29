import pygame
pygame.init()

screen_size = 640, 480

screen = pygame.display.set_mode(screen_size)

done = False
while done is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()

pygame.quit()
