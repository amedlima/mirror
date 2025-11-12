import pygame
import random
from constants import BLOCK, WALL_COLOR, ITEM_COLOR, GOAL_COLOR, WALL_HIGHLIGHT, WALL_SHADOW, ROOT_COLOR, MOSS_COLOR, APPLE_SHADOW, APPLE_SHINE, GOAL_GLOW

WALL  = 1
START = 2
ITEM  = 3
GOAL  = 4

class Map:
    def __init__(self, grid, offset = (0, 0), wall = WALL_COLOR, item = ITEM_COLOR, goal = GOAL_COLOR, with_walls = True):
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

    def render_forest_wall(self, screen, rect):
        """Draw a dirt/rock wall with roots - forest theme"""
        # Main dirt/bark texture
        pygame.draw.rect(screen, self.wall, rect)
        
        # Add 3D depth with highlights and shadows
        pygame.draw.line(screen, WALL_HIGHLIGHT, 
                        (rect.left, rect.top), (rect.right, rect.top), 2)
        pygame.draw.line(screen, WALL_HIGHLIGHT, 
                        (rect.left, rect.top), (rect.left, rect.bottom), 2)
        
        pygame.draw.line(screen, WALL_SHADOW, 
                        (rect.left, rect.bottom-1), (rect.right, rect.bottom-1), 2)
        pygame.draw.line(screen, WALL_SHADOW, 
                        (rect.right-1, rect.top), (rect.right-1, rect.bottom), 2)
        
        # Add root/crack pattern for forest feel
        if BLOCK >= 12:
            random.seed(rect.x + rect.y)  # Consistent pattern per block
            
            # Draw small roots/cracks
            for _ in range(2):
                start_x = rect.left + random.randint(2, rect.width - 4)
                start_y = rect.top + random.randint(2, rect.height - 4)
                end_x = start_x + random.randint(-3, 3)
                end_y = start_y + random.randint(2, 6)
                pygame.draw.line(screen, ROOT_COLOR, (start_x, start_y), (end_x, end_y), 1)
            
            # Add moss spots
            for _ in range(1):
                moss_x = rect.left + random.randint(2, rect.width - 3)
                moss_y = rect.top + random.randint(2, rect.height - 3)
                pygame.draw.circle(screen, MOSS_COLOR, (moss_x, moss_y), 2)

    def render_golden_apple(self, screen, rect):
        """Draw a golden apple collectible"""
        center_x, center_y = rect.center
        radius = rect.width // 2
        
        # Main golden apple body
        pygame.draw.circle(screen, self.item, (center_x, center_y), radius)
        
        # Add shadow on bottom right
        pygame.draw.circle(screen, APPLE_SHADOW, 
                         (center_x + 2, center_y + 2), radius - 2)
        
        # Add bright highlight on top left (shiny apple!)
        pygame.draw.circle(screen, APPLE_SHINE, 
                         (center_x - 2, center_y - 2), radius // 3)
        
        # Draw apple stem
        stem_x = center_x
        stem_y = center_y - radius
        pygame.draw.line(screen, (101, 67, 33), 
                        (stem_x, stem_y), (stem_x, stem_y - 3), 2)
        
        # Draw small leaf
        leaf_points = [
            (stem_x + 1, stem_y - 2),
            (stem_x + 4, stem_y - 3),
            (stem_x + 2, stem_y - 1)
        ]
        pygame.draw.polygon(screen, (107, 142, 35), leaf_points)

    def render_forest_goal(self, screen, rect):
        """Draw goal with forest/nature theme"""
        # Outer glow effect
        glow_rect = rect.inflate(6, 6)
        pygame.draw.rect(screen, GOAL_GLOW, glow_rect, border_radius=4)
        
        # Main goal area
        pygame.draw.rect(screen, self.goal, rect, border_radius=3)
        
        # Draw a tree/nature symbol in center
        cx, cy = rect.center
        size = rect.width // 3
        
        # Tree trunk
        pygame.draw.rect(screen, (101, 67, 33), 
                        (cx - 2, cy, 4, size))
        
        # Tree leaves (simple triangle)
        leaf_points = [
            (cx, cy - size),           # top
            (cx - size, cy),           # left
            (cx + size, cy)            # right
        ]
        pygame.draw.polygon(screen, (144, 238, 144), leaf_points)
        
        # Add sparkle effect
        sparkle_time = pygame.time.get_ticks() // 200
        if sparkle_time % 2 == 0:
            pygame.draw.circle(screen, (255, 255, 200), 
                             (cx - size//2, cy - size//2), 2)

    def render(self, screen):
        # Draw walls with forest texture
        for r in self.wall_rects:
            self.render_forest_wall(screen, r)
        
        # Draw golden apples
        for ir in self.item_rects:
            self.render_golden_apple(screen, ir)
        
        # Draw goal with tree symbol
        if self.goal_rect:
            self.render_forest_goal(screen, self.goal_rect)

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