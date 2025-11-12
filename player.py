import pygame
from constants import MOVE_STEP
from block import Block

class Player(Block):
    def __init__(self, width, height, color, x, y):
        super().__init__(x, y, color, width, height)
        self.sprite = self.create_forest_sprite(width, height, color)

    def create_forest_sprite(self, width, height, color):
        """Create a forest creature pixel art sprite (like a woodland animal)"""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        pixel_size = width // 5  # Divide into 5x5 pixel grid
        
        # Create a cute forest creature design
        if color[0] > color[2]:  # Red/Pink player - Fox character
            design = [
                # Ears
                (0,0,(255,140,0)), (4,0,(255,140,0)),
                # Head
                (1,1,(255,140,0)), (2,1,(255,140,0)), (3,1,(255,140,0)),
                (1,2,(255,180,100)), (2,2,(255,180,100)), (3,2,(255,180,100)),
                # Eyes
                (1,1,(50,50,50)), (3,1,(50,50,50)),
                # Nose
                (2,2,(50,50,50)),
                # Body
                (1,3,(255,140,0)), (2,3,(255,140,0)), (3,3,(255,140,0)),
                (1,4,(255,140,0)), (2,4,(255,140,0)), (3,4,(255,140,0)),
                # Belly (lighter)
                (2,3,(255,220,180)), (2,4,(255,220,180)),
            ]
        else:  # Blue player - Bluebird character
            design = [
                # Crest/feathers on top
                (2,0,(100,149,237)),
                # Head
                (1,1,(100,149,237)), (2,1,(100,149,237)), (3,1,(100,149,237)),
                # Eyes
                (1,1,(255,255,255)), (3,1,(255,255,255)),
                (1,1,(50,50,50)), (3,1,(50,50,50)),
                # Beak
                (4,2,(255,165,0)),
                # Body
                (1,2,(100,149,237)), (2,2,(100,149,237)), (3,2,(100,149,237)),
                (1,3,(135,206,250)), (2,3,(135,206,250)), (3,3,(135,206,250)),
                (1,4,(100,149,237)), (2,4,(100,149,237)), (3,4,(100,149,237)),
                # Wing detail
                (0,3,(70,130,180)), (4,3,(70,130,180)),
            ]
        
        for px, py, pixel_color in design:
            pygame.draw.rect(sprite, pixel_color, 
                           (px * pixel_size, py * pixel_size, pixel_size, pixel_size))
        
        return sprite

    def render(self, screen):
        """Draw the pixel sprite"""
        screen.blit(self.sprite, (self.x, self.y))

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