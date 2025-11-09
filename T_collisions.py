
def collision_barrier(player, barrier):
    if player.rect.colliderect(barrier.rect):
        print("collision barrier")
    #if player.rect.right > barrier.rect.left and player.rect.centerx < barrier.rect.centerx:
        #player.rect.left = barrier.rect.left

    #if player.rect.left < barrier.rect.right and player.rect.centerx > barrier.rect.centerx:
        #player.rect.right = barrier.rect.right

    #player.x, player.y = player.rect.x, player.rect.y
    #TWEAKING??? - problem is lowkey the frames and collisions

#dummy wall
def collision_wall(player, wall):
    if player.rect.colliderect(wall.rect):
        left_overlap = player.rect.right - wall.rect.left
        right_overlap = wall.rect.right - player.rect.left
        top_overlap = player.rect.bottom - wall.rect.top
        bottom_overlap = wall.rect.bottom - player.rect.top

        min_overlap = min(left_overlap, right_overlap, top_overlap, bottom_overlap)

        if min_overlap == left_overlap:
            player.rect.right = wall.rect.left
        elif min_overlap == right_overlap:
            player.rect.left = wall.rect.right
        elif min_overlap == top_overlap:
            player.rect.bottom = wall.rect.top
        else:
            player.rect.top = wall.rect.bottom


    player.x, player.y = player.rect.x, player.rect.y

def collision_screen(player, screen_width=300, screen_height=300):
    if player.rect.right>=screen_width:
        player.rect.right = screen_width

    if player.rect.left<=0:
        player.rect.left = 0

    if player.rect.bottom>=screen_height:
        player.rect.bottom = screen_height

    if player.rect.top<=0:
        player.rect.top = 0

    player.x, player.y = player.rect.x, player.rect.y






#ignore this i was testing some things

# if p2.rect.colliderect(barrier.rect):

#collide_players = p1.rect.colliderect(p2.rect)
#collide_with_barrier_p1 = p1.rect.colliderect(barrier.rect)
#collide_with_barrier_p2 = p2.rect.colliderect(barrier.rect)
#collide_with_wall_p1 = p1.rect.colliderect(wall_p1.rect)
#collide_with_wall_p2 = p2.rect.colliderect(wall_p2.rect)
#collide_with_screen_p1_sides = player.rect.right >= 300 or p1.rect.left <= 0
#collide_with_screen_p1_heads = player.rect.bottom > 300 or p1.rect.top <= 0

# checking collision
#if collide_players:
    #print("player collision detected")

#if collide_with_barrier_p1:
    #print("player 1 barrier collision detected")
#if collide_with_barrier_p2:
    #print("player 2 barrier collision detected")

#if collide_with_wall_p1:
    #print("player 1 wall collision detected")
#if collide_with_wall_p2:
    #print("player 2 wall collision detected")

#def collision_screen(collide_with_screen_p1_sides, collide_with_screen_p1_heads):
    #if collide_with_screen_p1_sides:

    #if collide_with_screen_p1_heads:
