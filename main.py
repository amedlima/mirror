import pygame
from constants import (BG_COLOR, MAZE_HEIGHT, MAZE_WIDTH, MARGIN, BLOCK, MOVE_STEP)
from player import Player
from map import Frame, Map


pygame.init()
screen = pygame.display.set_mode((1200, 800))
total_maze_width = MAZE_WIDTH * 2 + MARGIN
x_margin = (1200 - total_maze_width) // 2
y_margin = (800 - MAZE_HEIGHT) // 2
left_frame  = Frame(offset = (x_margin, y_margin))
right_frame = Frame(offset = (x_margin + MAZE_WIDTH + MARGIN, y_margin))

pygame.display.set_caption('mirror')

screen.fill(BG_COLOR)

pygame.display.flip()

p1 = Player(BLOCK, BLOCK, (255, 0, 0), 50, 50)
p2 = Player(BLOCK, BLOCK, (0, 0, 255), 200, 200)

map = Map()

def boundary_player (player, rect):
    r = pygame.Rect(player.x, player.y, player.width, player.height)
    r.clamp_ip (rect)
    player.x, player.y = r.x, r.y


# main loop
running = True
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
                
    boundary_player (p1, left_frame.player_rect())
    boundary_player (p2, right_frame.player_rect())

    screen.fill(BG_COLOR)
    left_frame.render(screen)
    right_frame.render(screen)
    p1.render(screen)
    p2.render(screen)

    pygame.display.flip()   # updates the screen
