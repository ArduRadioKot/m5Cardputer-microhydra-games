import time, random
from lib import display, userinput
from lib.hydra import config
from lib.hydra.beeper import Beeper
from font import vga1_8x16 as font
import machine


d = display.Display()
i = userinput.UserInput()
c = config.Config()
w, h = 240, 135

beep = Beeper()


BLOCK_WIDTH = 60  
BLOCK_HEIGHT = 12  
OUTLINE_WIDTH = 2  
INITIAL_SPEED = 1.0
MAX_SPEED = 5.0
SPEED_INCREASE = 0.05  
CAMERA_THRESHOLD = h // 2  

# Sound notes
SOUND_PLACE = ("G4", "B4")
SOUND_GAME_OVER = ("C3", "E3", "G3")
SOUND_SUCCESS = ("C4", "E4", "G4")
SOUND_PERFECT = ("C5", "E5", "G5")
SOUND_GOOD = ("C4", "E4")
SOUND_BAD = ("C3", "E3")

# Block colors
COLORS = [
    c.palette[8],  # White
    c.palette[1],  # Red
    c.palette[3],  # Green
    c.palette[4],  # Blue
    c.palette[5],  # Yellow
    c.palette[6],  # Magenta
    c.palette[7],  # Cyan
]

def play_sound(notes, duration=100):
    if c['ui_sound']:  
        beep.play(notes, duration, 10)  

def play_block_sound(overlap_ratio):
    if overlap_ratio > 0.9: 
        play_sound(SOUND_PERFECT, 150)
    elif overlap_ratio > 0.5: 
        play_sound(SOUND_GOOD, 100)
    else:  
        play_sound(SOUND_BAD, 80)

blocks = []
current_x = w // 2
current_width = BLOCK_WIDTH  
moving_right = True
score = 0
game_over = False
speed = INITIAL_SPEED
camera_y = 0  
last_time = time.ticks_ms()  

def draw_block(x, y, width, color):
    d.rect(
        int(x - width // 2 - OUTLINE_WIDTH),
        int(y + camera_y - OUTLINE_WIDTH),
        int(width + OUTLINE_WIDTH * 2),
        BLOCK_HEIGHT + OUTLINE_WIDTH * 2,
        c.palette[8]  # White outline
    )
    d.fill_rect(
        int(x - width // 2),
        int(y + camera_y),
        int(width),
        BLOCK_HEIGHT,
        color
    )

def draw_game_over():
    d.text("Game Over!", w//2 - 40, h//2 - 20, c.palette[4], font)
    d.text(f"Score: {score}", w//2 - 30, h//2 + 10, c.palette[8], font)
    d.text("Press ENTER", w//2 - 40, h//2 + 40, c.palette[7], font)

def reset_game():
    global blocks, current_x, current_width, moving_right, score, game_over, speed, camera_y, last_time
    blocks = []
    current_x = w // 2
    current_width = BLOCK_WIDTH
    moving_right = True
    score = 0
    game_over = False
    speed = INITIAL_SPEED
    camera_y = 0
    last_time = time.ticks_ms()

def get_random_color():
    return random.choice(COLORS)

def is_block_visible(y):
    screen_y = y + camera_y
    return 0 <= screen_y <= h

while True:
    current_time = time.ticks_ms()
    delta_time = time.ticks_diff(current_time, last_time) / 1000.0  
    last_time = current_time
    
    keys = i.get_new_keys()
    
    if game_over:
        if "ENT" in keys:
            reset_game()
            play_sound(SOUND_SUCCESS, 200)
        d.fill(c.palette[2])
        draw_game_over()
        d.show()
        time.sleep_ms(20)
        continue
    
    if not game_over:
        speed = min(MAX_SPEED, speed + SPEED_INCREASE * delta_time)
    
    if moving_right:
        current_x += speed
        if current_x + current_width // 2 >= w:
            moving_right = False
    else:
        current_x -= speed
        if current_x - current_width // 2 <= 0:
            moving_right = True
    
    if "ENT" in keys:
        if not blocks:  
            blocks.append([int(current_x), h - BLOCK_HEIGHT, BLOCK_WIDTH, get_random_color()])
            current_width = BLOCK_WIDTH  
            score += 1
            play_sound(SOUND_PLACE)
        else:
            prev_block = blocks[-1]
            prev_left = int(prev_block[0] - prev_block[2] // 2)
            prev_right = int(prev_block[0] + prev_block[2] // 2)
            current_left = int(current_x - current_width // 2)
            current_right = int(current_x + current_width // 2)
            
            overlap_left = max(prev_left, current_left)
            overlap_right = min(prev_right, current_right)
            overlap = int(overlap_right - overlap_left)
            
            if overlap <= 0:  
                game_over = True
                play_sound(SOUND_GAME_OVER, 500)
            else:   
                new_x = int((overlap_left + overlap_right) // 2)
                new_y = prev_block[1] - BLOCK_HEIGHT
                blocks.append([new_x, new_y, overlap, get_random_color()])
                current_width = overlap  
                score += 1
                
                overlap_ratio = overlap / prev_block[2]  
                play_block_sound(overlap_ratio)
                
                if new_y < CAMERA_THRESHOLD:
                    camera_y = CAMERA_THRESHOLD - new_y
    
    d.fill(c.palette[2])
    
    for block in blocks:
        if is_block_visible(block[1]):  
            draw_block(block[0], block[1], block[2], block[3])
    
    if not game_over:
        current_y = blocks[-1][1] - BLOCK_HEIGHT if blocks else h - BLOCK_HEIGHT
        if is_block_visible(current_y):  
            draw_block(current_x, current_y, current_width, c.palette[7])
    
    d.text(f"Score: {score}", 10, 10, c.palette[8], font)
    d.text(f"Speed: {speed:.1f}", 10, 30, c.palette[8], font)
    
    d.show()
    time.sleep_ms(20) 