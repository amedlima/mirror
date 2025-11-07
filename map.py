import pygame
from block import Block
from constants import BLOCK, MAZE_BLOCK,MAZE_WIDTH, MAZE_HEIGHT, ITEM_COLOR, GOAL_COLOR

class Frame:
    def __init__ (self, offset = (0, 0)):
        self.offset = offset
        ox, oy = self.offset
        self.bounds = pygame.Rect(ox, oy, MAZE_WIDTH, MAZE_HEIGHT)
        self.blocks = []

        cols = MAZE_WIDTH // BLOCK
        rows = MAZE_HEIGHT // BLOCK

        # top and bottom
        for c in range(cols):
            x = ox + c * BLOCK
            self.blocks.append(Block (x, oy, MAZE_BLOCK, BLOCK, BLOCK))
            self.blocks.append(Block(x, oy + (rows - 1) * BLOCK, MAZE_BLOCK, BLOCK, BLOCK))

        # left and right
        for r in range(rows):
            y = oy + r * BLOCK
            self.blocks.append(Block(ox, y, MAZE_BLOCK, BLOCK, BLOCK))                         
            self.blocks.append(Block(ox + (cols - 1) * BLOCK, y, MAZE_BLOCK, BLOCK, BLOCK))       

    def render (self, screen):
        for b in self.blocks:
            b.render(screen)

    def player_rect (self):
        return self.bounds.inflate(-2 * BLOCK, -2 * BLOCK)
    

class Map():
    def __init__(self):
        pass
    def render(self, screen):
        pygame.draw.rect(screen, self.bounds, width = MAZE_BLOCK)
