import time, random
from lib import display, userinput
from lib.hydra import config
from lib.hydra.beeper import Beeper
import machine

d = display.Display()
i = userinput.UserInput()
c = config.Config()
w, h = 240, 135

beep = Beeper()

# Game constants
GRID_SIZE = 4           # 4x4 pixel cells
GRID_WIDTH = 32         # 128px / 4
GRID_HEIGHT = 16        # 64px / 4
BORDER = 16             # 16px border
INITIAL_DELAY = 200     # ms between moves
DELAY_DECREMENT = 5     # ms speed increase per 10 points

# Colors (using config palette)
COLOR_SNAKE_HEAD = c.palette[3]  # Green
COLOR_SNAKE_BODY = c.palette[11] # Dark green
COLOR_FOOD = c.palette[1]        # Red
COLOR_BG = c.palette[2]          # Background
COLOR_TEXT = c.palette[8]        # White
COLOR_BORDER = c.palette[0]      # Black

# Sound notes
SOUND_EAT = ("C5", "E5")
SOUND_GAME_OVER = ("C3", "E3", "G3")
SOUND_START = ("C4", "E4", "G4")

class Snake:
    def __init__(self):
        self.segments = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (1, 0)  # Start moving right
        self.next_direction = self.direction
        self.grow = False
    
    def update_direction(self):
        self.direction = self.next_direction
    
    def move(self):
        self.update_direction()
        head_x, head_y = self.segments[0]
        new_head = (
            (head_x + self.direction[0]) % GRID_WIDTH,
            (head_y + self.direction[1]) % GRID_HEIGHT
        )
        self.segments.insert(0, new_head)
        if not self.grow:
            self.segments.pop()
        else:
            self.grow = False

class SnakeGame:
    def __init__(self):
        self.state = "START"  # START, PLAY, GAME_OVER
        self.snake = Snake()
        self.food = (0, 0)
        self.score = 0
        self.delay = INITIAL_DELAY
        self.last_move_time = time.ticks_ms()
        self.generate_food()
    
    def generate_food(self):
        while True:
            self.food = (
                random.randint(0, GRID_WIDTH-1),
                random.randint(0, GRID_HEIGHT-1)
            )
            if self.food not in self.snake.segments:
                break
    
    def handle_input(self, keys):
        if self.state == "PLAY":
            if "UP" in keys and self.snake.direction != (0, 1):
                self.snake.next_direction = (0, -1)
            elif "DOWN" in keys and self.snake.direction != (0, -1):
                self.snake.next_direction = (0, 1)
            elif "LEFT" in keys and self.snake.direction != (1, 0):
                self.snake.next_direction = (-1, 0)
            elif "RIGHT" in keys and self.snake.direction != (-1, 0):
                self.snake.next_direction = (1, 0)
            elif "A" in keys:
                self.state = "START"
        
        elif self.state == "START" and "ENT" in keys:
            self.state = "PLAY"
            self.last_move_time = time.ticks_ms()
            play_sound(SOUND_START)
        
        elif self.state == "GAME_OVER" and "ENT" in keys:
            self.__init__()  # Reset game
    
    def update(self):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_move_time) >= self.delay:
            self.snake.move()
            self.last_move_time = current_time
            
            # Check collisions
            head = self.snake.segments[0]
            # Check self collision
            if head in self.snake.segments[1:]:
                self.state = "GAME_OVER"
                play_sound(SOUND_GAME_OVER)
                return
            
            # Check food collision
            if head == self.food:
                self.snake.grow = True
                self.score += 1
                # Increase speed every 10 points
                if self.score % 10 == 0:
                    self.delay = max(50, self.delay - DELAY_DECREMENT)
                play_sound(SOUND_EAT)
                self.generate_food()
    
    def render(self):
        d.fill(COLOR_BG)
        
        # Draw play area border
        d.rect(BORDER-1, BORDER-1, 130, 66, COLOR_BORDER)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake.segments):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            d.fill_rect(
                BORDER + x * GRID_SIZE,
                BORDER + y * GRID_SIZE,
                GRID_SIZE, GRID_SIZE, color
            )
        
        # Draw food
        fx, fy = self.food
        d.fill_rect(
            BORDER + fx * GRID_SIZE,
            BORDER + fy * GRID_SIZE,
            GRID_SIZE, GRID_SIZE, COLOR_FOOD
        )
        
        # Draw score
        d.text(f"Score: {self.score}", BORDER + 5, 5, COLOR_TEXT)
        
        # Draw game state messages
        if self.state == "START":
            d.text("SNAKE", w//2 - 30, h//2 - 20, COLOR_TEXT)
            d.text("Press ENTER", w//2 - 40, h//2 + 10, COLOR_TEXT)
        elif self.state == "GAME_OVER":
            d.text("GAME OVER", w//2 - 40, h//2 - 20, COLOR_TEXT)
            d.text(f"Score: {self.score}", w//2 - 30, h//2 + 10, COLOR_TEXT)
            d.text("Press ENTER", w//2 - 40, h//2 + 40, COLOR_TEXT)

def play_sound(notes, duration=100):
    if c['ui_sound']:  
        beep.play(notes, duration, 10)

def main():
    game = SnakeGame()
    
    while True:
        keys = i.get_new_keys()
        game.handle_input(keys)
        
        if game.state == "PLAY":
            game.update()
        
        game.render()
        d.show()
        time.sleep_ms(10)

if __name__ == "__main__":
    main()