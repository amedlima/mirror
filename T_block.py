import pygame

class Block:
    def __init__(self, x, y, color, width, height):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Barrier:
    def __init__(self,x,y,colour, width, height):
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))


#dummy wall to test collisions
class Wall:
    def __init__(self, x, y, colour, width, height):
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))



