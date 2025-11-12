import pygame
import random
import math
from constants import SKY_TOP, SKY_BOTTOM, MARGIN, BLOCK, GROUND_COLOR, MOSS_COLOR, CLOUD_WHITE, CLOUD_SHADOW, TEXT_COLOR, TEXT_OUTLINE
from player import Player
from map import Map
from mazes import MAZES 

LEFT, RIGHT = MAZES 

class Cloud:
    """Parallax cloud for depth effect"""
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.surface = self.create_cloud()
    
    def create_cloud(self):
        """Create a pixel art cloud"""
        width = self.size * 40
        height = self.size * 20
        cloud = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # puffy cloud shape
        for i in range(3):
            x = i * (width // 4) + width // 6
            y = height // 2
            radius = self.size * 8 + random.randint(-3, 3)
            pygame.draw.circle(cloud, CLOUD_WHITE, (x, y), radius)
        
        return cloud
    
    def update(self, screen_width):
        self.x += self.speed
        if self.x > screen_width + 100:
            self.x = -100
    
    def draw(self, screen):
        screen.blit(self.surface, (int(self.x), int(self.y)))

def create_forest_background(width, height):
    """Create a forest-themed pixel art background with sky gradient"""
    bg = pygame.Surface((width, height))
    
    # Sky gradient (top to bottom)
    for y in range(height):
        ratio = y / height
        r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * ratio)
        g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * ratio)
        b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * ratio)
        pygame.draw.line(bg, (r, g, b), (0, y), (width, y))
    
    # ground grass texture at bottom
    grass_height = 80
    for y in range(height - grass_height, height):
        # Wavy grass pattern
        for x in range(0, width, 4):
            grass_shade = random.choice([GROUND_COLOR, MOSS_COLOR])
            blade_height = random.randint(3, 8)
            pygame.draw.rect(bg, grass_shade, (x, y, 3, blade_height))
    
    # small decorative elements 
    random.seed(42)
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(height - 60, height - 20)
        # Small flowers
        pygame.draw.circle(bg, (255, 150, 150), (x, y), 3)
        pygame.draw.rect(bg, (100, 200, 100), (x-1, y+2, 2, 8))
    

    # Add background trees
    for _ in range(10):
        x = random.randint(0, width)
        y = random.randint(height - 100, height - 100)
        # Tree trunk
        pygame.draw.rect(bg, (101, 67, 33), (x, y, 8, 40))
        # Tree leaves
        pygame.draw.circle(bg, (34, 139, 34), (x + 4, y), 20)
    return bg

def draw_text(surface, text, font, x, y, text_color, center=True):
    """Draw text with black outline for better readability"""
    
    # Draw main text
    text_surf = font.render(text, True, text_color)
    if center:
        text_rect = text_surf.get_rect(center=(x, y))
    else:
        text_rect = text_surf.get_rect(topleft=(x, y))
    surface.blit(text_surf, text_rect)
    
    return text_rect

# Initialize Pygame and sound
pygame.init()
pygame.mixer.init()

# Create sound effects (8-bit style using pure tones)
def create_move_sound():
    """Create a simple beep for movement"""
    sample_rate = 22050
    duration = 0.05
    frequency = 440
    samples = int(sample_rate * duration)
    wave = [int(32767 * 0.3 * math.sin(2 * math.pi * frequency * t / sample_rate)) 
            for t in range(samples)]
    sound = pygame.sndarray.make_sound(pygame.array.array('h', wave))
    return sound

def create_collect_sound():
    """Create a rising tone for collecting items"""
    sample_rate = 22050
    duration = 0.15
    samples = int(sample_rate * duration)
    wave = []
    for t in range(samples):
        frequency = 440 + (t / samples) * 440  # Rise from 440Hz to 880Hz
        wave.append(int(32767 * 0.3 * math.sin(2 * math.pi * frequency * t / sample_rate)))
    sound = pygame.sndarray.make_sound(pygame.array.array('h', wave))
    return sound

def create_win_sound():
    """Create a victory jingle"""
    sample_rate = 22050
    duration = 0.5
    samples = int(sample_rate * duration)
    wave = []
    notes = [523, 659, 784, 1047]  # C, E, G, C (major chord)
    for t in range(samples):
        note_index = int((t / samples) * len(notes))
        if note_index >= len(notes):
            note_index = len(notes) - 1
        frequency = notes[note_index]
        wave.append(int(32767 * 0.2 * math.sin(2 * math.pi * frequency * t / sample_rate)))
    sound = pygame.sndarray.make_sound(pygame.array.array('h', wave))
    return sound

# Load sounds
try:
    move_sound = create_move_sound()
    collect_sound = create_collect_sound()
    win_sound = create_win_sound()
    sounds_enabled = True
except:
    sounds_enabled = False
    print("Sound not available")

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption('Forest Maze')

# Create forest background
background = create_forest_background(900, 600)

# Create clouds for parallax effect
clouds = [
    Cloud(random.randint(0, 900), random.randint(20, 250), 0.3, 1.2),
    Cloud(random.randint(0, 900), random.randint(30, 220), 0.5, 1.5),
    Cloud(random.randint(0, 900), random.randint(40, 200), 0.2, 1.0),
    Cloud(random.randint(0, 900), random.randint(50, 240), 0.4, 2.0),
]

# Try to load retro pixel font, fallback to system fonts
font_large = None
font_medium = None

# Try multiple retro fonts
retro_fonts = ['Press Start 2P']
for font_name in retro_fonts:
    try:
        font_large = pygame.font.SysFont(font_name, 60, bold=True)
        font_medium = pygame.font.SysFont(font_name, 38, bold=True)
        print(f"Using font: {font_name}")
        break
    except:
        continue

# Fallback
if font_large is None:
    font_large = pygame.font.Font(None, 68)
    font_medium = pygame.font.Font(None, 38)

# Map setup
left_columns, left_rows = len(LEFT["maze"][0]), len(LEFT["maze"])
right_columns, right_rows = len(RIGHT["maze"][0]), len(RIGHT["maze"])
left_width, left_height = left_columns * BLOCK, left_rows * BLOCK
right_width, right_height = right_columns * BLOCK, right_rows * BLOCK

total_width = left_width + MARGIN + right_width
x_margin = (900 - total_width) // 2
y_margin = (600 - max(left_height, right_height)) // 2

left_offset  = (x_margin, y_margin)
right_offset = (x_margin + left_width + MARGIN, y_margin)
left_map  = Map(LEFT["maze"], offset = left_offset)
right_map = Map(RIGHT["maze"], offset = right_offset)

# Players
p1 = Player(BLOCK, BLOCK, (255, 100, 100), left_map.start_position()[0], left_map.start_position()[1])
p2 = Player(BLOCK, BLOCK, (100, 100, 255), right_map.start_position()[0], right_map.start_position()[1])

score_left = 0
score_right = 0
game_over = False
win_sound_played = False

# Goal states
right_goal_active  = True
left_goal_active   = False
right_goal_reached = False
left_goal_reached  = False

def boundary_player(player, rect):
    r = pygame.Rect(player.x, player.y, player.width, player.height)
    r.clamp_ip(rect)
    player.x, player.y = r.x, r.y

# Main loop
running = True
clock = pygame.time.Clock()
last_move_time = 0
move_cooldown = 100  # ms between move sounds

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    # Movement
    keys = pygame.key.get_pressed()
    moved=False
    
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
    
    # Play move sound
    if moved and sounds_enabled and current_time - last_move_time > move_cooldown:
        move_sound.play()
        last_move_time = current_time

    boundary_player(p1, left_map.bounds())
    boundary_player(p2, right_map.bounds())

    # Collect items
    if left_map.collect_items(p1.rect()):
        score_left += 10
        if sounds_enabled:
            collect_sound.play()
    if right_map.collect_items(p2.rect()):
        score_right += 10
        if sounds_enabled:
            collect_sound.play()

    # Goal logic
    if right_goal_active and right_map.reached_goal(p2.rect()):
        right_goal_reached = True
        right_goal_active  = False
        left_goal_active   = True

    if left_goal_active and left_map.reached_goal(p1.rect()):
        left_goal_reached = True
        left_goal_active  = False

    if right_goal_reached and left_goal_reached and not game_over:
        game_over = True
        if sounds_enabled and not win_sound_played:
            win_sound.play()
            win_sound_played = True

    # Draw everything
    screen.blit(background, (0, 0))
    
    # Update and draw clouds (parallax)
    for cloud in clouds:
        cloud.update(900)
        cloud.draw(screen)
    
    # Draw maps and players
    left_map.render(screen)
    if hasattr(left_map, "goal_rect") and not left_goal_active and not left_goal_reached:
        gx, gy, gw, gh = left_map.goal_rect
        pygame.draw.line(screen, (120, 120, 120), (gx, gy), (gx+gw, gy+gh), 3)
        pygame.draw.line(screen, (120, 120, 120), (gx+gw, gy), (gx, gy+gh), 3)
    
    right_map.render(screen)
    p1.render(screen)
    p2.render(screen)

    # Score display
    score_text = f"Left: {score_left}  |  Right: {score_right}"
    draw_text(screen, score_text, font_medium, 450, 90, TEXT_COLOR)

    # Messages
    if not right_goal_reached:
        draw_text(screen, "Reach the right goal first!", 
                             font_large, 450, 30, TEXT_COLOR)
    elif not left_goal_reached:
        draw_text(screen, "Now reach the left goal!", 
                             font_large, 450, 30, TEXT_COLOR)
    else:
        draw_text(screen, "You Win! Press ESC to quit", 
                             font_large, 450, 30, TEXT_COLOR)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()