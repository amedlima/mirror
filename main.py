import pygame
from constants import BG_COLOR
from player import Player
from map import Map

screen = pygame.display.set_mode((300, 300))

pygame.display.set_caption('mirror')

screen.fill(BG_COLOR)

pygame.display.flip()

running = True

p1 = Player(20, 20, (255, 0, 0), 50, 50)
p2 = Player(20, 20, (0, 0, 255), 200, 200)

map = Map()

# main loop
while running:
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            p1.move("up")
            p2.move("down")
        if keys[pygame.K_s]:
            p1.move("down")
            p2.move("up")
        if keys[pygame.K_a]:
            p1.move("left")
            p2.move("right")
        if keys[pygame.K_d]:
            p1.move("right")
            p2.move("left")
                
    screen.fill(BG_COLOR)
    p1.render(screen)
    p2.render(screen)

    pygame.display.flip()   # updates the screen