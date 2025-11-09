import pygame
from constants import MOVE_STEP
from T_block import Block


class Player(Block):
    def __init__(self, width, height, color, x, y):
        super().__init__(x, y, color, width, height)

    def move(self, direction):
        if direction == "up":
            self.y -= MOVE_STEP
            self.rect.y -= MOVE_STEP
        elif direction == "down":
            self.y += MOVE_STEP
            self.rect.y += MOVE_STEP
        elif direction == "left":
            self.x -= MOVE_STEP
            self.rect.x -= MOVE_STEP
        elif direction == "right":
            self.x += MOVE_STEP
            self.rect.x += MOVE_STEP



