import pygame
from constants import MOVE_STEP
from block import Block

class Player(Block):
    def __init__(self, width, height, color, x, y):
        super().__init__(x, y, color, width, height)

    def move(self, direction, maze = None):
        dx = dy = 0
        if direction == "up":
            dy -= MOVE_STEP
        elif direction == "down":
            dy += MOVE_STEP
        elif direction == "left":
            dx -= MOVE_STEP         
        elif direction == "right":
            dx += MOVE_STEP

        if maze is not None:
            new_rect = pygame.Rect(self.x + dx, self.y + dy, self.width, self.height)
            if not maze.can_move(new_rect):
                return False
        
        self.x += dx
        self.y += dy
        return True