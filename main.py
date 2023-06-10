import pygame as pg
from random import randrange

pg.init()

WINDOW = 700 
TITLE_SIZE = 30
RANGE = (TITLE_SIZE // 2, WINDOW - TITLE_SIZE // 2, TITLE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg. rect.Rect([0, 0, TITLE_SIZE -2, TITLE_SIZE -2])
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
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

def draw():
    # vẽ lại các phần tử đã thay đổi
    screen.fill('black')
    pg.draw.rect(screen, food_color , food)
    [pg.draw.rect(screen, 'green', segment) for segment in segments]

    # hiển thị điểm số trên màn hình
    font = pg.font.SysFont('Arial', 23)
    text = font.render(f'Score: {score}', True, 'white')
    text_rect = text.get_rect(topright=(WINDOW - 5, 5))
    screen.blit(text, text_rect)

    pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -TITLE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, TITLE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TITLE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (TITLE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    # di chuyển rắn
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

        # kiểm tra va chạm
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
            snake.center, food.center = get_random_position(), get_random_position()
            length, snake_dir = 1, (0, 0)
            segments = [snake.copy()]

        # Kiểm tra thức ăn
        if snake.center == food.center:
            if food_color == 'red':
                food_count += 1
                if food_count >= 5:
                    food_color = 'yellow'
                    food_count = 0
            else:
                food_color = 'red'
            food.center = get_random_position()
            length += 1
        
        # tính điểm
        score = (length - 1) * 5

        # hiển thị trò chơi và điểm số
        draw()

    # tối ưu tốc độ game
    clock.tick(60)