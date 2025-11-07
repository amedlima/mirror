import pygame

class Block:
    def __init__(self, x, y, color, width, height):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))