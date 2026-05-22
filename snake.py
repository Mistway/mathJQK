"""贪食蛇 (Snake) 游戏

使用 pygame 实现的经典贪食蛇小游戏。

操作说明:
    方向键 / WASD  : 控制蛇的移动方向
    空格 / P       : 暂停 / 继续
    R              : 游戏结束后重新开始
    Esc            : 退出游戏

运行:
    pip install pygame
    python snake.py
"""

import random
import sys

import pygame

# ----------------------------- 配置 ----------------------------- #
CELL_SIZE = 20          # 每个格子的像素大小
COLS, ROWS = 30, 20     # 横向、纵向格子数量
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
FPS = 10                # 初始速度 (帧 / 秒)

# 颜色 (R, G, B)
BG_COLOR = (18, 18, 18)
GRID_COLOR = (30, 30, 30)
SNAKE_HEAD_COLOR = (0, 200, 0)
SNAKE_BODY_COLOR = (0, 150, 0)
FOOD_COLOR = (220, 50, 50)
TEXT_COLOR = (240, 240, 240)

# 方向向量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_food(snake):
    """在不与蛇身重叠的位置随机生成食物。"""
    available = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake]
    if not available:
        return None  # 蛇已填满整个棋盘 (通关)
    return random.choice(available)


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))


def draw_cell(surface, pos, color):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BG_COLOR, rect, 1)  # 描边


def draw_text(surface, text, size, center, color=TEXT_COLOR):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, color)
    rect = img.get_rect(center=center)
    surface.blit(img, rect)


def reset_game():
    """返回初始状态: 蛇、方向、食物、得分。"""
    mid = (COLS // 2, ROWS // 2)
    snake = [mid, (mid[0] - 1, mid[1]), (mid[0] - 2, mid[1])]
    direction = RIGHT
    food = random_food(snake)
    score = 0
    return snake, direction, food, score


def main():
    pygame.init()
    pygame.display.set_caption("贪食蛇 Snake")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    snake, direction, food, score = reset_game()
    next_direction = direction
    speed = FPS
    paused = False
    game_over = False

    key_to_dir = {
        pygame.K_UP: UP, pygame.K_w: UP,
        pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
        pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
        pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_SPACE, pygame.K_p) and not game_over:
                    paused = not paused
                if event.key == pygame.K_r and game_over:
                    snake, direction, food, score = reset_game()
                    next_direction = direction
                    speed = FPS
                    game_over = False
                if event.key in key_to_dir and not game_over and not paused:
                    new_dir = key_to_dir[event.key]
                    # 禁止 180° 反向
                    if (new_dir[0] + direction[0], new_dir[1] + direction[1]) != (0, 0):
                        next_direction = new_dir

        if not paused and not game_over:
            direction = next_direction
            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])

            # 撞墙
            if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
                game_over = True
            # 撞到自身 (移动后尾部会让位, 所以排除最后一节)
            elif new_head in snake[:-1]:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    speed = min(FPS + score // 3, 30)  # 每吃 3 个加速一档, 最高 30 FPS
                    food = random_food(snake)
                    if food is None:
                        game_over = True  # 通关
                else:
                    snake.pop()

        # ---------- 绘制 ---------- #
        screen.fill(BG_COLOR)
        draw_grid(screen)
        if food is not None:
            draw_cell(screen, food, FOOD_COLOR)
        for i, segment in enumerate(snake):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            draw_cell(screen, segment, color)

        draw_text(screen, f"Score: {score}", 28, (60, 16))

        if paused:
            draw_text(screen, "PAUSED", 64, (WIDTH // 2, HEIGHT // 2))
            draw_text(screen, "Press Space/P to resume", 28, (WIDTH // 2, HEIGHT // 2 + 50))
        if game_over:
            draw_text(screen, "GAME OVER", 64, (WIDTH // 2, HEIGHT // 2 - 20))
            draw_text(screen, f"Final Score: {score}", 32, (WIDTH // 2, HEIGHT // 2 + 30))
            draw_text(screen, "Press R to restart, Esc to quit", 24, (WIDTH // 2, HEIGHT // 2 + 70))

        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
