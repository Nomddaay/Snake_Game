import pygame as pg
from random import randrange

pg.init()

WINDOW = 700 
TITLE_SIZE = 30
RANGE = (TITLE_SIZE // 2, WINDOW - TITLE_SIZE // 2, TITLE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TITLE_SIZE -2, TITLE_SIZE -2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
food_color = 'red'
food_count = 0
screen = pg.display.set_mode([WINDOW]*2)
clock = pg.time.Clock()
score = 0

#tải âm thanh
chomp_sound = pg.mixer.Sound('pop.wav')

def draw_game():
    # vẽ lại các phần tử đã thay đổi
    screen.fill('black')
    pg.draw.rect(screen, food_color , food)

    for segment in segments:
        pg.draw.rect(screen, 'green', segment)

    # vẽ điểm số lên màn hình
    font = pg.font.SysFont('Arial', 23)
    text = font.render(f'Score: {score}', True, 'white')
    text_rect = text.get_rect(topright=(WINDOW - 5, 5))
    screen.blit(text, text_rect)

    # vẽ mắt cho con rắn
    left_eye = pg.Rect(snake.centerx - 8, snake.centery - 10, 5, 5)
    right_eye = pg.Rect(snake.centerx + 3, snake.centery - 10, 5, 5)
    pg.draw.rect(screen, 'black', left_eye)
    pg.draw.rect(screen, 'black', right_eye)

    pg.display.update()

def check_collision():
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW:
        return True

    if snake.collidelist(segments[:-1]) != -1:
        return True

    return False

def draw_game_over():
    # Vẽ màn hình đen mờ
    dim_screen = pg.Surface(screen.get_size()).convert_alpha()
    dim_screen.fill((0, 0, 0, 180))
    screen.blit(dim_screen, (0, 0))

    # Vẽ chữ "Game Over"
    font = pg.font.SysFont('Arial', 60)
    game_over_text = font.render('GAME OVER', True, 'white')
    game_over_rect = game_over_text.get_rect(center=(WINDOW // 2, WINDOW // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Vẽ điểm số
    font = pg.font.SysFont('Arial', 30)
    score_text = font.render(f'Score: {score}', True, 'white')
    score_rect = score_text.get_rect(center=(WINDOW // 2, WINDOW // 2))
    screen.blit(score_text, score_rect)

    pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and snake_dir != (0, TITLE_SIZE):
                snake_dir = (0, -TITLE_SIZE)
            elif event.key == pg.K_s and snake_dir != (0, -TITLE_SIZE):
                snake_dir = (0, TITLE_SIZE)
            elif event.key == pg.K_a and snake_dir != (TITLE_SIZE, 0):
                snake_dir = (-TITLE_SIZE, 0)
            elif event.key == pg.K_d and snake_dir != (-TITLE_SIZE, 0):
                snake_dir = (TITLE_SIZE, 0)

    # di chuyển rắn
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

    # kiểm tra va chạm
    if check_collision():
        draw_game_over()  # hiển thị màn hình "Game Over" và điểm số
        pg.time.wait(3000)  # đợi 1.5 giây trước khi thoát
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
        food_color = 'red'
        food_count = 0
        score = 0

    # Kiểm tra thức ăn
    if snake.center == food.center:
        chomp_sound.play()
        if food_color == 'red':
            food_count += 1
            if food_count >= 5:
                food_color = 'yellow'
                food_count = 0
        else:
            food_color = 'red'
            score += 15 #thêm điểm khi ăn con mồi vàng
        food.center = get_random_position()
        length += 1
    
    # tính điểm
    if food_color == 'red':
        score = (length - 1) * 5

        # hiển thị trò chơi và điểm số
    draw_game()

    # tối ưu tốc độ game
    clock.tick(60)