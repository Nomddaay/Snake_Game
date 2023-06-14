import pygame as pg
from random import randrange

pg.init()

WINDOW_SIZE = 700
TITLE_SIZE = 30
RANGE = (TITLE_SIZE // 2, WINDOW_SIZE - TITLE_SIZE // 2, TITLE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.Rect(0, 0, TITLE_SIZE - 2, TITLE_SIZE - 2)
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time = 0
time_step = 110
food = snake.copy()
food.center = get_random_position()
food_color = 'red'
food_count = 0
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pg.time.Clock()
score = 0
best_score = 0

# Tải âm thanh
pg.mixer.init()
chomp_sound = pg.mixer.Sound('hiss.wav')


def draw_game():
    screen.fill('#8B4513')
    pg.draw.rect(screen, food_color, food)

    for segment in segments:
        pg.draw.rect(screen, 'green', segment)

    font = pg.font.SysFont('Arial', 23)
    text = font.render(f'Score: {score}', True, 'white')
    text_rect = text.get_rect(topright=(WINDOW_SIZE - 5, 5))
    screen.blit(text, text_rect)

    best_text = font.render(f'Best Score: {best_score}', True, 'white')
    best_rect = best_text.get_rect(topright=(WINDOW_SIZE - 5, 35))
    screen.blit(best_text, best_rect)

    left_eye = pg.Rect(snake.centerx - 8, snake.centery - 10, 5, 5)
    right_eye = pg.Rect(snake.centerx + 3, snake.centery - 10, 5, 5)
    pg.draw.rect(screen, 'black', left_eye)
    pg.draw.rect(screen, 'black', right_eye)

    pg.display.update()


def check_collision():
    if snake.collidelist(segments[:-1]) != -1:
        return True

    return False


def draw_game_over():
    dim_screen = pg.Surface(screen.get_size()).convert_alpha()
    dim_screen.fill((0, 0, 0, 180))
    screen.blit(dim_screen, (0, 0))

    font = pg.font.SysFont('Arial', 60)
    game_over_text = font.render('GAME OVER', True, 'white')
    game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    font = pg.font.SysFont('Arial', 30)
    score_text = font.render(f'Score: {score}', True, 'white')
    score_rect = score_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(score_text, score_rect)

    best_text = font.render(f'Best Score: {best_score}', True, 'white')
    best_rect = best_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 40))
    screen.blit(best_text, best_rect)

    pg.display.update()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and snake_dir != (0, TITLE_SIZE):
                snake_dir = (0, -TITLE_SIZE)
                time_step = 90  # Giảm thời gian chờ khi di chuyển lên
            elif event.key == pg.K_s and snake_dir != (0, -TITLE_SIZE):
                snake_dir = (0, TITLE_SIZE)
                time_step = 90  # Giảm thời gian chờ khi di chuyển xuống
            elif event.key == pg.K_a and snake_dir != (TITLE_SIZE, 0):
                snake_dir = (-TITLE_SIZE, 0)
                time_step = 110  # Khôi phục thời gian chờ mặc định cho di chuyển sang trái
            elif event.key == pg.K_d and snake_dir != (-TITLE_SIZE, 0):
                snake_dir = (TITLE_SIZE, 0)
                time_step = 110  # Khôi phục thời gian chờ mặc định cho di chuyển sang phải

    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        if snake.left < 0:
            snake.right = WINDOW_SIZE
        elif snake.right > WINDOW_SIZE:
            snake.left = 0
        elif snake.top < 0:
            snake.bottom = WINDOW_SIZE
        elif snake.bottom > WINDOW_SIZE:
            snake.top = 0

        segments.append(snake.copy())
        segments = segments[-length:]

        if check_collision():
            if score > best_score:
                best_score = score
            draw_game_over()
            pg.time.wait(3000)
            snake.center, food.center = get_random_position(), get_random_position()
            while any(segment.colliderect(food) for segment in segments):
                food.center = get_random_position()
            length, snake_dir = 1, (0, 0)
            segments = [snake.copy()]
            food_color = 'red'
            food_count = 0
            score = 0

        if snake.center == food.center:
            chomp_sound.play()
            if food_color == 'red':
                food_count += 1
                if food_count >= 5:
                    food_color = 'yellow'
                    food_count = 0
            else:
                food_color = 'red'
                score += 15
            food.center = get_random_position()
            while any(segment.colliderect(food) for segment in segments):
                food.center = get_random_position()
            length += 1

        if food_color == 'red':
            score = (length - 1) * 5

    draw_game()
    clock.tick(60)
