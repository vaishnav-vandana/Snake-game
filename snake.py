import pygame
import random
import os
import time

# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()
pygame.mixer.init()

# ============================================================
# SCREEN
# ============================================================

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Adventure")

clock = pygame.time.Clock()

# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
RED = (230, 50, 50)
GREEN = (40, 200, 80)
DARK_GREEN = (20, 120, 50)
YELLOW = (255, 220, 50)
PINK = (231, 84, 128)
BLUE = (50, 150, 255)
PURPLE = (170, 70, 220)
GRAY = (100, 100, 110)
DARK_GRAY = (35, 35, 45)
ORANGE = (255, 150, 40)

# ============================================================
# FONTS
# ============================================================

FONT_SMALL = pygame.font.SysFont("arial", 24)
FONT_MEDIUM = pygame.font.SysFont("arial", 35, bold=True)
FONT_LARGE = pygame.font.SysFont("arial", 55, bold=True)
FONT_TITLE = pygame.font.SysFont("arial", 75, bold=True)

# ============================================================
# GAME SETTINGS
# ============================================================

SNAKE_SIZE = 20

START_X = 100
START_Y = 100

START_SPEED = 8
MAX_SPEED = 18

# ============================================================
# FILE PATHS
# ============================================================

BACKGROUND_PATH = r"i:\MUSIC AND PHOTOS\download.jfif"
MUSIC_PATH = r"i:\MUSIC AND PHOTOS\background music.mp3"
EAT_SOUND_PATH = r"i:\MUSIC AND PHOTOS\eating sound.mp3"
GAMEOVER_SOUND_PATH = r"i:\MUSIC AND PHOTOS\mario_game_over_sms.mp3"

HIGHSCORE_FILE = "highscore.txt"

# ============================================================
# LOAD BACKGROUND
# ============================================================

try:
    background = pygame.image.load(BACKGROUND_PATH)
    background = pygame.transform.scale(
        background,
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
except:
    background = None


# ============================================================
# LOAD SOUNDS SAFELY
# ============================================================

def play_music():
    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
    except:
        pass


def play_eat_sound():
    try:
        sound = pygame.mixer.Sound(EAT_SOUND_PATH)
        sound.play()
    except:
        pass


def play_gameover_sound():
    try:
        pygame.mixer.music.load(GAMEOVER_SOUND_PATH)
        pygame.mixer.music.play()
    except:
        pass


# ============================================================
# HIGH SCORE
# ============================================================

def load_highscore():

    if not os.path.exists(HIGHSCORE_FILE):

        with open(HIGHSCORE_FILE, "w") as file:
            file.write("0")

        return 0

    try:
        with open(HIGHSCORE_FILE, "r") as file:
            return int(file.read())
    except:
        return 0


def save_highscore(score):

    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(score))


# ============================================================
# TEXT FUNCTION
# ============================================================

def draw_text(text, font, color, x, y, center=False):

    image = font.render(text, True, color)

    if center:

        rect = image.get_rect(center=(x, y))
        screen.blit(image, rect)

    else:

        screen.blit(image, (x, y))


# ============================================================
# BUTTON
# ============================================================

def draw_button(text, x, y, width, height):

    rect = pygame.Rect(x, y, width, height)

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        color = BLUE
    else:
        color = DARK_GRAY

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        2,
        border_radius=12
    )

    draw_text(
        text,
        FONT_MEDIUM,
        WHITE,
        x + width // 2,
        y + height // 2,
        True
    )

    return rect


# ============================================================
# DRAW BACKGROUND
# ============================================================

def draw_background():

    if background:

        screen.blit(background, (0, 0))

        # Dark transparent overlay
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 80))

        screen.blit(overlay, (0, 0))

    else:

        screen.fill(BLACK)


# ============================================================
# CREATE FOOD
# ============================================================

def create_food(snake, obstacles):

    while True:

        x = random.randrange(
            0,
            SCREEN_WIDTH - SNAKE_SIZE,
            SNAKE_SIZE
        )

        y = random.randrange(
            80,
            SCREEN_HEIGHT - SNAKE_SIZE,
            SNAKE_SIZE
        )

        position = (x, y)

        if position not in snake and position not in obstacles:

            food_type = random.choice(
                ["normal", "gold", "speed"]
            )

            return {
                "x": x,
                "y": y,
                "type": food_type
            }


# ============================================================
# FOOD DRAWING
# ============================================================

def draw_food(food):

    x = food["x"]
    y = food["y"]

    center = (
        x + SNAKE_SIZE // 2,
        y + SNAKE_SIZE // 2
    )

    if food["type"] == "normal":

        pygame.draw.circle(
            screen,
            RED,
            center,
            SNAKE_SIZE // 2
        )

        # Highlight
        pygame.draw.circle(
            screen,
            WHITE,
            (x + 7, y + 6),
            3
        )

    elif food["type"] == "gold":

        pygame.draw.circle(
            screen,
            YELLOW,
            center,
            SNAKE_SIZE // 2
        )

        pygame.draw.circle(
            screen,
            ORANGE,
            center,
            SNAKE_SIZE // 2,
            2
        )

    elif food["type"] == "speed":

        pygame.draw.circle(
            screen,
            BLUE,
            center,
            SNAKE_SIZE // 2
        )

        pygame.draw.line(
            screen,
            WHITE,
            (x + 5, y + 10),
            (x + 12, y + 10),
            3
        )

        pygame.draw.line(
            screen,
            WHITE,
            (x + 12, y + 10),
            (x + 9, y + 5),
            3
        )


# ============================================================
# CREATE OBSTACLES
# ============================================================

def create_obstacles(level):

    obstacles = []

    number = min(4 + level * 2, 20)

    for _ in range(number):

        for attempt in range(100):

            x = random.randrange(
                2,
                SCREEN_WIDTH // SNAKE_SIZE - 2
            ) * SNAKE_SIZE

            y = random.randrange(
                5,
                SCREEN_HEIGHT // SNAKE_SIZE - 2
            ) * SNAKE_SIZE

            new_obstacle = (x, y)

            # Don't put obstacles near starting position
            if x < 300 and y < 250:
                continue

            if new_obstacle not in obstacles:

                obstacles.append(new_obstacle)
                break

    return obstacles


# ============================================================
# DRAW OBSTACLES
# ============================================================

def draw_obstacles(obstacles):

    for x, y in obstacles:

        rect = pygame.Rect(
            x,
            y,
            SNAKE_SIZE,
            SNAKE_SIZE
        )

        pygame.draw.rect(
            screen,
            PURPLE,
            rect,
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            WHITE,
            rect,
            1,
            border_radius=4
        )


# ============================================================
# DRAW SNAKE
# ============================================================

def draw_snake(snake, direction):

    for index, (x, y) in enumerate(snake):

        rect = pygame.Rect(
            x,
            y,
            SNAKE_SIZE,
            SNAKE_SIZE
        )

        # HEAD
        if index == len(snake) - 1:

            pygame.draw.rect(
                screen,
                YELLOW,
                rect,
                border_radius=6
            )

            # Eyes
            if direction == "RIGHT":

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 14, y + 5),
                    3
                )

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 14, y + 15),
                    3
                )

            elif direction == "LEFT":

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 6, y + 5),
                    3
                )

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 6, y + 15),
                    3
                )

            elif direction == "UP":

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 5, y + 6),
                    3
                )

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 15, y + 6),
                    3
                )

            else:

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 5, y + 14),
                    3
                )

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x + 15, y + 14),
                    3
                )

        # BODY
        else:

            pygame.draw.rect(
                screen,
                PINK,
                rect,
                border_radius=5
            )


# ============================================================
# HUD
# ============================================================

def draw_hud(score, highscore, level, lives):

    pygame.draw.rect(
        screen,
        (0, 0, 0, 170),
        (0, 0, SCREEN_WIDTH, 65)
    )

    draw_text(
        f"Score: {score}",
        FONT_SMALL,
        WHITE,
        20,
        18
    )

    draw_text(
        f"High Score: {highscore}",
        FONT_SMALL,
        YELLOW,
        190,
        18
    )

    draw_text(
        f"Level: {level}",
        FONT_SMALL,
        BLUE,
        430,
        18
    )

    draw_text(
        f"Lives: {'❤ ' * lives}",
        FONT_SMALL,
        RED,
        600,
        18
    )

    draw_text(
        "P = Pause",
        FONT_SMALL,
        WHITE,
        1000,
        18
    )


# ============================================================
# PAUSE SCREEN
# ============================================================

def pause_screen():

    overlay = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 180))

    screen.blit(overlay, (0, 0))

    draw_text(
        "GAME PAUSED",
        FONT_TITLE,
        YELLOW,
        SCREEN_WIDTH // 2,
        280,
        True
    )

    draw_text(
        "Press P to continue",
        FONT_MEDIUM,
        WHITE,
        SCREEN_WIDTH // 2,
        360,
        True
    )

    pygame.display.update()


# ============================================================
# WELCOME SCREEN
# ============================================================

def welcome():

    running = True

    while running:

        draw_background()

        # Title
        draw_text(
            "SNAKE ADVENTURE",
            FONT_TITLE,
            YELLOW,
            SCREEN_WIDTH // 2,
            170,
            True
        )

        draw_text(
            "A new generation of the classic Snake game",
            FONT_SMALL,
            WHITE,
            SCREEN_WIDTH // 2,
            230,
            True
        )

        start_button = draw_button(
            "START GAME",
            440,
            320,
            320,
            70
        )

        draw_text(
            "Arrow Keys  •  Eat Food  •  Avoid Obstacles",
            FONT_SMALL,
            WHITE,
            SCREEN_WIDTH // 2,
            440,
            True
        )

        draw_text(
            "Normal Food = 10    Gold = 30    Speed = 20",
            FONT_SMALL,
            YELLOW,
            SCREEN_WIDTH // 2,
            480,
            True
        )

        draw_text(
            "Press SPACE to start",
            FONT_SMALL,
            WHITE,
            SCREEN_WIDTH // 2,
            550,
            True
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    play_music()
                    return True

                if event.key == pygame.K_ESCAPE:
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if start_button.collidepoint(event.pos):
                        play_music()
                        return True

        pygame.display.update()
        clock.tick(30)

    return False


# ============================================================
# GAME OVER SCREEN
# ============================================================

def game_over_screen(score, highscore):

    play_gameover_sound()

    while True:

        draw_background()

        draw_text(
            "GAME OVER",
            FONT_TITLE,
            RED,
            SCREEN_WIDTH // 2,
            180,
            True
        )

        draw_text(
            f"Your Score: {score}",
            FONT_LARGE,
            WHITE,
            SCREEN_WIDTH // 2,
            290,
            True
        )

        draw_text(
            f"High Score: {highscore}",
            FONT_MEDIUM,
            YELLOW,
            SCREEN_WIDTH // 2,
            350,
            True
        )

        restart_button = draw_button(
            "PLAY AGAIN",
            440,
            430,
            320,
            65
        )

        draw_text(
            "Press ENTER to play again",
            FONT_SMALL,
            WHITE,
            SCREEN_WIDTH // 2,
            540,
            True
        )

        draw_text(
            "Press ESC to quit",
            FONT_SMALL,
            GRAY,
            SCREEN_WIDTH // 2,
            580,
            True
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    play_music()
                    return "restart"

                if event.key == pygame.K_ESCAPE:
                    return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if restart_button.collidepoint(event.pos):
                        play_music()
                        return "restart"

        pygame.display.update()
        clock.tick(30)


# ============================================================
# MAIN GAME
# ============================================================

def game_loop():

    highscore = load_highscore()

    snake = [
        (START_X - 40, START_Y),
        (START_X - 20, START_Y),
        (START_X, START_Y)
    ]

    direction = "RIGHT"
    next_direction = "RIGHT"

    score = 0
    lives = 3

    level = 1

    speed = START_SPEED

    obstacles = create_obstacles(level)

    food = create_food(snake, obstacles)

    running = True
    paused = False

    while running:

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "quit"

                if event.key == pygame.K_p:

                    paused = not paused

                    if paused:
                        pause_screen()

                if not paused:

                    if event.key == pygame.K_UP and direction != "DOWN":
                        next_direction = "UP"

                    elif event.key == pygame.K_DOWN and direction != "UP":
                        next_direction = "DOWN"

                    elif event.key == pygame.K_LEFT and direction != "RIGHT":
                        next_direction = "LEFT"

                    elif event.key == pygame.K_RIGHT and direction != "LEFT":
                        next_direction = "RIGHT"

        # ====================================================
        # PAUSED
        # ====================================================

        if paused:

            pause_screen()
            clock.tick(10)
            continue

        # ====================================================
        # MOVE SNAKE
        # ====================================================

        direction = next_direction

        head_x, head_y = snake[-1]

        if direction == "RIGHT":
            head_x += SNAKE_SIZE

        elif direction == "LEFT":
            head_x -= SNAKE_SIZE

        elif direction == "UP":
            head_y -= SNAKE_SIZE

        elif direction == "DOWN":
            head_y += SNAKE_SIZE

        new_head = (head_x, head_y)

        # ====================================================
        # WALL COLLISION
        # ====================================================

        wall_collision = (
            head_x < 0
            or head_x >= SCREEN_WIDTH
            or head_y < 65
            or head_y >= SCREEN_HEIGHT
        )

        # ====================================================
        # SELF COLLISION
        # ====================================================

        self_collision = new_head in snake

        # ====================================================
        # OBSTACLE COLLISION
        # ====================================================

        obstacle_collision = new_head in obstacles

        if wall_collision or self_collision or obstacle_collision:

            lives -= 1

            if lives <= 0:

                if score > highscore:
                    highscore = score
                    save_highscore(highscore)

                result = game_over_screen(
                    score,
                    highscore
                )

                return result

            else:

                # Reset snake position
                snake = [
                    (START_X - 40, START_Y),
                    (START_X - 20, START_Y),
                    (START_X, START_Y)
                ]

                direction = "RIGHT"
                next_direction = "RIGHT"

                pygame.time.delay(500)

                continue

        # ====================================================
        # ADD NEW HEAD
        # ====================================================

        snake.append(new_head)

        # ====================================================
        # FOOD COLLISION
        # ====================================================

        food_position = (
            food["x"],
            food["y"]
        )

        if new_head == food_position:

            play_eat_sound()

            if food["type"] == "normal":

                score += 10

            elif food["type"] == "gold":

                score += 30

            elif food["type"] == "speed":

                score += 20

                speed = min(
                    speed + 1,
                    MAX_SPEED
                )

            # High score
            if score > highscore:

                highscore = score
                save_highscore(highscore)

            # Level increases every 50 points
            new_level = score // 50 + 1

            if new_level > level:

                level = new_level

                speed = min(
                    START_SPEED + level,
                    MAX_SPEED
                )

                obstacles = create_obstacles(level)

            food = create_food(
                snake,
                obstacles
            )

        else:

            # Remove tail
            snake.pop(0)

        # ====================================================
        # DRAW
        # ====================================================

        draw_background()

        # Play area border
        pygame.draw.rect(
            screen,
            WHITE,
            (
                0,
                65,
                SCREEN_WIDTH,
                SCREEN_HEIGHT - 65
            ),
            2
        )

        draw_obstacles(obstacles)

        draw_food(food)

        draw_snake(
            snake,
            direction
        )

        draw_hud(
            score,
            highscore,
            level,
            lives
        )

        pygame.display.update()

        # ====================================================
        # GAME SPEED
        # ====================================================

        clock.tick(speed)

    return "quit"


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    while True:

        start_game = welcome()

        if not start_game:
            break

        result = game_loop()

        if result == "quit":
            break

        if result == "restart":
            continue

    pygame.quit()


# ============================================================
# START
# ============================================================

main()
