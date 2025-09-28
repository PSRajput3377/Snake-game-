# snake_game.py
# Simple Snake game using pygame
# Requires: pip install pygame

import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("Snake Game - by Prashant")

# ----- Config -----
WIDTH, HEIGHT = 640, 480
CELL = 20
FPS = 10
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BG_COLOR = (30,30,30)

# ----- Init -----
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

def draw_text(surface, text, pos, color=WHITE):
    img = font.render(text, True, color)
    surface.blit(img, pos)

def random_cell():
    x = random.randrange(0, WIDTH, CELL)
    y = random.randrange(0, HEIGHT, CELL)
    return x, y

class Snake:
    def __init__(self):
        self.body = [(WIDTH//2, HEIGHT//2), (WIDTH//2 - CELL, HEIGHT//2), (WIDTH//2 - 2*CELL, HEIGHT//2)]
        self.dir = (CELL, 0)  # moving right
        self.grow_pending = 0

    def head(self):
        return self.body[0]

    def move(self):
        new_head = (self.head()[0] + self.dir[0], self.head()[1] + self.dir[1])
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def change_dir(self, new_dir):
        # Prevent reversing
        if (new_dir[0] == -self.dir[0] and new_dir[1] == -self.dir[1]):
            return
        self.dir = new_dir

    def grow(self):
        self.grow_pending += 1

    def collides_with_self(self):
        return self.head() in self.body[1:]

    def collides_with_wall(self):
        x, y = self.head()
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT

def main():
    snake = Snake()
    food = random_cell()
    score = 0
    running = True
    paused = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r:
                    # restart
                    snake = Snake()
                    food = random_cell()
                    score = 0
                    paused = False

                # directions: arrow keys & WASD
                if event.key in (pygame.K_UP, pygame.K_w):
                    snake.change_dir((0, -CELL))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.change_dir((0, CELL))
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.change_dir((-CELL, 0))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.change_dir((CELL, 0))

        if paused:
            draw_centered(screen, "PAUSED - Press 'P' to resume")
            pygame.display.flip()
            continue

        snake.move()

        # eat food?
        if snake.head() == food:
            score += 10
            snake.grow()
            # keep generating food until it doesn't spawn on snake
            while True:
                food = random_cell()
                if food not in snake.body:
                    break

        # collisions
        if snake.collides_with_wall() or snake.collides_with_self():
            # game over screen
            game_over_screen(screen, score)
            # wait for R to restart or ESC to quit
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_r:
                            snake = Snake()
                            food = random_cell()
                            score = 0
                            waiting = False
                        elif e.key == pygame.K_ESCAPE:
                            pygame.quit(); sys.exit()

        # draw
        screen.fill(BG_COLOR)

        # draw grid (optional)
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))

        # draw snake
        for i, seg in enumerate(snake.body):
            rect = pygame.Rect(seg[0], seg[1], CELL, CELL)
            color = GREEN if i == 0 else (0,170,0)
            pygame.draw.rect(screen, color, rect)

        # draw food
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

        # HUD
        draw_text(screen, f"Score: {score}", (10, 10))
        draw_text(screen, "Press P to pause | R to restart | Esc to quit", (10, HEIGHT - 30), color=(180,180,180))

        pygame.display.flip()

def draw_centered(surface, text):
    s = font.render(text, True, WHITE)
    r = s.get_rect(center=(WIDTH//2, HEIGHT//2))
    surface.blit(s, r)

def game_over_screen(surface, score):
    surface.fill(BG_COLOR)
    draw_text(surface, "GAME OVER", (WIDTH//2 - 80, HEIGHT//2 - 40))
    draw_text(surface, f"Final score: {score}", (WIDTH//2 - 90, HEIGHT//2))
    draw_text(surface, "Press R to restart or Esc to quit", (WIDTH//2 - 170, HEIGHT//2 + 40))
    pygame.display.flip()

if __name__ == "__main__":
    main()
