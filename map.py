import pygame
from constants import BLOCK, BLOCK_COLOR, ITEM_COLOR, GOAL_COLOR


WALL  = 1
START = 2
ITEM  = 3
GOAL  = 4

class Map:
    def __init__(self, grid, offset = (0, 0), wall = BLOCK_COLOR, item = ITEM_COLOR, goal = GOAL_COLOR, with_walls = True):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.offset = offset
        self.wall = wall
        self.item = item
        self.goal = goal
        self.with_walls = with_walls

        ox, oy = offset
        self.wall_rects = []
        self.item_rects = []
        self.start_cell = (0, 0)
        self.goal_rect = None

        pad = max(2, BLOCK // 6)

        for gy, row in enumerate(grid):
            for gx, cell in enumerate(row):
                x = ox + gx * BLOCK
                y = oy + gy * BLOCK
                if cell == WALL and with_walls:
                    self.wall_rects.append(pygame.Rect(x, y, BLOCK, BLOCK))
                elif cell == START:
                    self.start_cell = (gx, gy)
                elif cell == ITEM:
                    self.item_rects.append(pygame.Rect(x + pad, y + pad, BLOCK - 2*pad, BLOCK - 2*pad))
                elif cell == GOAL:
                    self.goal_rect = pygame.Rect(x + pad, y + pad, BLOCK - 2*pad, BLOCK - 2*pad)

        self.pixel_rect = pygame.Rect(ox, oy, self.cols * BLOCK, self.rows * BLOCK)


    def render(self, screen):
        for r in self.wall_rects:
            pygame.draw.rect(screen, self.wall, r)
        for ir in self.item_rects:
            pygame.draw.rect(screen, self.item, ir)
        if self.goal_rect:
            pygame.draw.rect(screen, self.goal, self.goal_rect)


    def bounds(self) -> pygame.Rect:
        return self.pixel_rect


    def start_position(self):
        gx, gy = self.start_cell
        return (self.offset[0] + gx * BLOCK, self.offset[1] + gy * BLOCK)


    def goal_position(self):
        return self.goal_rect.topleft if self.goal_rect else None


    def can_move(self, rect: pygame.Rect) -> bool:
        if not self.pixel_rect.contains(rect):
            return False
        return not any(rect.colliderect(w) for w in self.wall_rects)


    def collect_items(self, rect: pygame.Rect) -> bool:
        for i, ir in enumerate(self.item_rects):
            if rect.colliderect(ir):
                del self.item_rects[i]
                return True
        return False
    

    def reached_goal(self, rect: pygame.Rect) -> bool:
        return self.goal_rect is not None and rect.colliderect(self.goal_rect)
    

    #def render(self, screen)
    #    pygame.draw.rect(screen, self.bounds, width = MAZE_BLOCK)
