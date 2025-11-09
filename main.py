import pygame
from constants import BG_COLOR, MARGIN, BLOCK, MOVE_STEP
from player import Player
from map import Map
from mazes import MAZES 
LEFT, RIGHT = MAZES 


pygame.font.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('mirror')
screen.fill(BG_COLOR)
font = pygame.font.SysFont('Arial', 24)
pygame.display.flip()

left_columns, left_rows = len(LEFT["maze"][0]), len(LEFT["maze"])
right_columns, right_rows = len(RIGHT["maze"][0]), len(RIGHT["maze"])
left_width, left_height = left_columns * BLOCK, left_rows * BLOCK
right_width, right_height = right_columns * BLOCK, right_rows * BLOCK

total_width = left_width + MARGIN + right_width
x_margin = (900 - total_width) // 2
y_margin = (600 - max (left_height, right_height)) // 2

left_offset  = (x_margin, y_margin)
right_offset = (x_margin + left_width + MARGIN, y_margin)
left_map  = Map(LEFT["maze"], offset = left_offset)
right_map = Map(RIGHT["maze"], offset = right_offset)


p1 = Player(BLOCK, BLOCK, (255, 0, 0), left_map.start_position()[0], left_map.start_position()[1])
p2 = Player(BLOCK, BLOCK, (0, 0, 255), right_map.start_position()[0], right_map.start_position()[1])

score_left = 0
score_right = 0

# after the right goal is reached, left can get to its goal
right_goal_active  = True
left_goal_active   = False
right_goal_reached = False
left_goal_reached  = False


def blink (alpha_speed = 6):
    t = pygame.time.get_ticks() // alpha_speed
    return 60 + 60 * ((t % 40) < 20) 

def boundary_player (player, rect):
    r = pygame.Rect(player.x, player.y, player.width, player.height)
    r.clamp_ip (rect)
    player.x, player.y = r.x, r.y

def message_box(screen, font, text, anchor_rect, under=True, gap = 10):
    message = font.render(text, True, (20, 20, 20))
    message_rect = message.get_rect()
    message_rect.midtop = (anchor_rect.midbottom[0], anchor_rect.midbottom[1] + gap)
    pygame.draw.rect(screen, (255, 255, 255), message_rect.inflate(20, 6), border_radius = 8)
    screen.blit(message, message_rect)

def score_box():
    score_text = f"Left Score: {score_left}   Right Score: {score_right}"
    score_surf = font.render(score_text, True, (20, 20, 20))
    score_rect = score_surf.get_rect(midtop = (screen.get_width() // 2, 20))
    pygame.draw.rect(screen, (255, 255, 255), score_rect.inflate(12, 6), border_radius = 8)
    screen.blit(score_surf, score_rect)
    return score_rect


# main loop
running = True
while running:
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            p1.move("up", left_map)
            p2.move("down", right_map)
        if keys[pygame.K_s]:
            p1.move("down", left_map)
            p2.move("up", right_map)
        if keys[pygame.K_a]:
            p1.move("left", left_map)
            p2.move("right", right_map)
        if keys[pygame.K_d]:
            p1.move("right", left_map)
            p2.move("left", right_map)

    boundary_player (p1, left_map.bounds())
    boundary_player (p2, right_map.bounds())

    if left_map.collect_items(p1.rect()):
        score_left += 10
    if right_map.collect_items(p2.rect()):
        score_right += 10

    if right_goal_active and right_map.reached_goal(p2.rect()):
        right_goal_reached = True
        right_goal_active  = False
        left_goal_active   = True          

    if left_goal_active and left_map.reached_goal(p1.rect()):
        left_goal_reached = True
        left_goal_active  = False

    if right_goal_reached and left_goal_reached and not game_over:
        game_over = True


    screen.fill(BG_COLOR)
    left_map.render(screen)
    if hasattr(left_map, "goal_rect") and not left_goal_active and not left_goal_reached:
        gx, gy, gw, gh = left_map.goal_rect
        pygame.draw.line(screen, (120,120,120), (gx,gy), (gx+gw,gy+gh), 3)
        pygame.draw.line(screen, (120,120,120), (gx+gw,gy), (gx,gy+gh), 3)
    right_map.render(screen)
    p1.render(screen)
    p2.render(screen)

    score_rect = score_box()

    if not right_goal_reached:
        message_box(screen, font, "Reach the right goal to activate the left goal", score_rect, under = True, gap = 20)
    elif not left_goal_reached:
        message_box(screen, font, "Now reach the left goal to finish the game", score_rect, under = True, gap = 20)
    else:
        message_box(screen, font, "Congratulations! You have completed the game!", score_rect, under = True, gap = 20)

    pygame.display.flip()   # updates the screen
