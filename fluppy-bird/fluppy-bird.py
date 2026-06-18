import time, random

from lib import display, userinput
from lib.hydra import config
# Beeper может отсутствовать или работать иначе, убираем на время отладки
# from lib.hydra.beeper import Beeper 

d = display.Display()
i = userinput.UserInput()
c = config.Config()

# Константы размера экрана из документации
w, h = 240, 135

# Настройки игры (оставляем как есть, но убираем звуки)
BIRD_WIDTH = 15 # Сделаем чуть меньше
BIRD_HEIGHT = 10
PIPE_WIDTH = 30
PIPE_GAP = 60 # Уменьшим зазор для лучшей видимости на малом экране
PIPE_SPEED = 2 # Увеличим скорость для динамики
GRAVITY = 0.5
FLAP_STRENGTH = -4 # Уменьшим силу прыжка
SCROLL_SPEED = 1

# Цвета из палитры конфигурации
BG_COLOR = c.palette[1]    # Синий фон
BIRD_COLOR = c.palette[5]  # Желтый
PIPE_COLOR = c.palette[3]  # Зеленый
TEXT_COLOR = c.palette[8]  # Белый
GROUND_COLOR = c.palette[6] # Коричневая земля

# Убираем функцию play_sound и звуковые константы

class Bird:
    def __init__(self):
        self.x = w // 3
        self.y = h // 2
        self.velocity = 0
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT

    def update(self):
        # Применяем гравитацию
        self.velocity += GRAVITY
        self.y += self.velocity

        # Проверка выхода за границы экрана (упрощаем)
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > h - self.height:
            self.y = h - self.height
            self.velocity = 0
            return True  # Упал на "землю"
        return False

    def flap(self):
        self.velocity = FLAP_STRENGTH
        # play_sound(SOUND_FLAP) # Убираем звук

    def draw(self):
        # Рисуем птицу как заполненный прямоугольник
        d.fill_rect(int(self.x), int(self.y), self.width, self.height, BIRD_COLOR)
        # Простой глаз - точка
        d.fill_rect(int(self.x) + self.width - 4, int(self.y) + 2, 2, 2, c.palette[0]) # Черный глаз

class Pipe:
    def __init__(self, x):
        self.x = x
        # Убедимся, что зазор помещается
        min_y = 20
        max_y = h - 20 - PIPE_GAP
        if min_y < max_y:
             self.gap_y = random.randint(min_y, max_y)
        else:
             self.gap_y = h // 2 - PIPE_GAP // 2 # На случай, если экран слишком мал

        self.passed = False
        self.width = PIPE_WIDTH

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Верхняя труба (от верха экрана до зазора)
        if self.gap_y > 0:
            d.fill_rect(int(self.x), 0, self.width, int(self.gap_y), PIPE_COLOR)
        # Нижняя труба (от конца зазора до низа экрана)
        bottom_pipe_top = self.gap_y + PIPE_GAP
        bottom_pipe_height = h - int(bottom_pipe_top)
        if bottom_pipe_height > 0:
            d.fill_rect(int(self.x), int(bottom_pipe_top), self.width, bottom_pipe_height, PIPE_COLOR)

    def collides_with(self, bird):
        bird_rect = (int(bird.x), int(bird.y), bird.width, bird.height)
        # Верхняя труба
        top_pipe_rect = (int(self.x), 0, self.width, int(self.gap_y))
        # Нижняя труба
        bottom_pipe_top = self.gap_y + PIPE_GAP
        bottom_pipe_rect = (int(self.x), int(bottom_pipe_top), self.width, h - int(bottom_pipe_top))

        # Проверка пересечения прямоугольников
        if self._rects_intersect(bird_rect, top_pipe_rect) or self._rects_intersect(bird_rect, bottom_pipe_rect):
            return True
        return False

    def _rects_intersect(self, rect1, rect2):
        """Проверяет пересечение двух прямоугольников (x, y, w, h)"""
        r1x, r1y, r1w, r1h = rect1
        r2x, r2y, r2w, r2h = rect2
        return not (r1x + r1w <= r2x or r2x + r2w <= r1x or r1y + r1h <= r2y or r2y + r2h <= r1y)


def reset_game():
    global bird, pipes, score, game_over, last_pipe_time

    bird = Bird()
    pipes = []
    score = 0
    game_over = False
    last_pipe_time = time.ticks_ms()

def draw_background():
    # Фон
    d.fill(BG_COLOR)
    # Простая "земля" внизу
    d.fill_rect(0, h - 5, w, 5, GROUND_COLOR)

def draw_game_over():
    # Используем базовый метод text из документации
    # Параметры: text, x, y, color
    try:
        # Попробуем вывести текст, если метод поддерживает только базовые параметры
        d.text("GAME OVER", w//2 - 40, h//2 - 20, TEXT_COLOR)
        d.text(f"SCORE: {score}", w//2 - 30, h//2, TEXT_COLOR)
        d.text("PRESS ENT", w//2 - 35, h//2 + 20, TEXT_COLOR)
    except:
        # Если с позиционированием проблемы, просто базовый вывод
        d.fill(BG_COLOR) # Очистим снова
        d.text("GAME OVER", 10, 10, TEXT_COLOR)
        d.text(f"SCORE: {score}", 10, 30, TEXT_COLOR)
        d.text("PRESS ENT", 10, 50, TEXT_COLOR)


# Инициализация игры
reset_game()

# Основной игровой цикл
while True:
    # Получаем ввод
    keys = i.get_new_keys()

    # Очистка экрана на каждой итерации
    draw_background()

    if game_over:
        draw_game_over()
        d.show()
        # Проверяем перезапуск
        if "ENT" in keys:
            reset_game()
        time.sleep_ms(50) # Можно чуть увеличить задержку на экране game over
        continue # Пропускаем остальную логику обновления

    # Управление
    # Используем только поддерживаемые клавиши
    if "ENT" in keys: # Используем ENT для прыжка
        bird.flap()

    # Обновление птицы
    if bird.update(): # Если птица упала
        game_over = True
        # play_sound(SOUND_DIE, 300) # Убираем звук

    # Генерация новых труб
    current_time = time.ticks_ms()
    if current_time - last_pipe_time > 2000: # Каждые 2 секунды
        pipes.append(Pipe(w))
        last_pipe_time = current_time

    # Обновление и отрисовка труб
    for pipe in pipes[:]: # Итерация по копии списка
        pipe.update()

        # Проверка столкновения
        if pipe.collides_with(bird):
            game_over = True
            # play_sound(SOUND_HIT, 200) # Убираем звук
            # Не break, просто помечаем game_over. Столкновение отрисуется в этом кадре.

        # Проверка прохождения трубы (начисление очков)
        if not pipe.passed and pipe.x + pipe.width < bird.x:
            pipe.passed = True
            score += 1
            # play_sound(SOUND_SCORE, 100) # Убираем звук

        # Удаление труб за пределами экрана
        if pipe.x + pipe.width < 0:
            pipes.remove(pipe)
            continue # Уже удален, не рисуем

        # Отрисовка трубы (если не удалена)
        pipe.draw()

    # Отрисовка птицы
    bird.draw()

    # Отрисовка счета
    try:
        d.text(f"SCORE: {score}", 10, 10, TEXT_COLOR)
    except:
         d.text(f"{score}", 10, 10, TEXT_COLOR) # Если длинный текст не поддерживается

    # Обновление экрана
    d.show()

    # Небольшая задержка для контроля FPS
    time.sleep_ms(30)
