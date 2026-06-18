# Flappy Bird для Cardputer

## Описание игры

Flappy Bird - это классическая аркадная игра, где вы управляете птицей, которая должна пролетать между зелеными трубами. Цель - пролететь как можно дальше, не задевая препятствия!

### Особенности реализации:
- Аутентичная физика полета птицы
- Случайная генерация препятствий
- Система подсчета очков
- Звуковые эффекты для ключевых событий
- Простая, но узнаваемая графика

## Как играть

1. Птица постоянно падает вниз под действием гравитации
2. Нажимайте **ENTER** или **SPACE**, чтобы птица взмахнула крыльями и поднялась вверх
3. Пролетайте между трубами, не задевая их
4. Каждая успешно пройденная пара труб приносит 1 очко
5. Игра заканчивается при столкновении с трубой или землей

### Управление:
- **ENTER/SPACE** - взмах крыльев (прыжок вверх)
- **ENTER** на экране Game Over - начать заново

## Технические требования

- **Оборудование**: Cardputer
- **Прошивка**: MicroHydra
- **Дисплей**: 240x135 пикселей
- **Требуется**: 
  - Устройство ввода (кнопки)
  - Динамик для звуковых эффектов

## Настройка сложности

Вы можете изменить параметры игры в начале кода:

```python
# Настройки сложности
PIPE_SPEED = 1.5    # Скорость движения труб
PIPE_GAP = 70       # Расстояние между трубами
GRAVITY = 0.4       # Сила гравитации
FLAP_STRENGTH = -6  # Сила прыжка
```

## Автор

[Ваше имя/никнейм]

## Лицензия

[MIT License] - свободное использование и модификация кода

---

# Flappy Bird for Cardputer (English version)

## Game Description

Flappy Bird is a classic arcade game where you control a bird that must fly between green pipes. The goal is to fly as far as possible without hitting obstacles!

### Features:
- Authentic bird flight physics
- Random obstacle generation
- Score system
- Sound effects for key events
- Simple but recognizable graphics

## How to Play

1. The bird constantly falls due to gravity
2. Press **ENTER** or **SPACE** to make the bird flap its wings and rise up
3. Fly between pipes without touching them
4. Each successfully passed pipe pair gives 1 point
5. Game ends when hitting a pipe or the ground

### Controls:
- **ENTER/SPACE** - flap wings (jump up)
- **ENTER** on Game Over screen - restart

## Technical Requirements

- **Hardware**: Cardputer
- **Firmware**: MicroHydra
- **Display**: 240x135 pixels
- **Requires**:
  - Input device (buttons)
  - Speaker for sound effects

## Difficulty Settings

You can adjust game parameters in the code:

```python
# Difficulty settings
PIPE_SPEED = 1.5    # Pipe movement speed
PIPE_GAP = 70       # Gap between pipes
GRAVITY = 0.4       # Gravity force
FLAP_STRENGTH = -6  # Jump strength
```

## Author

[Your name/nickname]

## License

[MIT License] - free to use and modify