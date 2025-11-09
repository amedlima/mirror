import pygame
from constants import *
from player import Player
from map import Map
from T_block import Barrier
from T_block import Wall
from T_collisions import *


pygame.init()

screen = pygame.display.set_mode((300, 300))

pygame.display.set_caption('mirror')

screen.fill(BG_COLOR)

pygame.display.flip()

running = True

p1 = Player(20, 20, (255, 0, 0), 50, 50)
p2 = Player(20, 20, (0, 0, 255), 200, 200)
barrier = Barrier(145, 0, (0, 255, 0), 10, 300)
wall_p1 = Wall(50, 30, (0, 0, 255), 60, 10)
wall_p2 = Wall(200, 30, (255, 0, 0), 60, 10)



#surfaces=graphics

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


    collision_barrier(p1 , barrier)
    collision_barrier(p2, barrier)
    collision_wall(p1, wall_p1)
    collision_wall(p2, wall_p2)
    collision_screen(p1, screen_width=300, screen_height=300)
    collision_screen(p2, screen_width=300, screen_height=300)


    screen.fill(BG_COLOR)
    barrier.render(screen)
    p1.render(screen)
    p2.render(screen)
    wall_p1.render(screen)
    wall_p2.render(screen)
    pygame.display.flip()   # updates the screen