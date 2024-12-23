import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Running Man')

clock = pygame.time.Clock()

background = pygame.image.load('jungle.jpg')  # Jungle background image
player_img = pygame.image.load('player.png')  # Player image
obstacle_img = pygame.image.load('obstacle.png')  # Obstacle image

background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = pygame.transform.scale(player_img, (50, 50))
obstacle_img = pygame.transform.scale(obstacle_img, (30, 50))

player_size = 50
player_x = 100
player_y = SCREEN_HEIGHT - player_size
player_velocity_y = 0
GRAVITY = 1
jump_strength = -15

obstacle_width = 30
obstacle_height = 50
obstacles = []
obstacle_speed = 10
SPAWN_INTERVAL = 1500  # in milliseconds
last_spawn_time = pygame.time.get_ticks()

score = 0
font = pygame.font.Font(None, 36)

running = True

def draw_player(x, y):
    screen.blit(player_img, (x, y))


def draw_obstacle(x, y):
    screen.blit(obstacle_img, (x, y))


def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y == SCREEN_HEIGHT - player_size:
                player_velocity_y = jump_strength

    player_y += player_velocity_y
    if player_y < SCREEN_HEIGHT - player_size:
        player_velocity_y += GRAVITY
    else:
        player_y = SCREEN_HEIGHT - player_size
        player_velocity_y = 0

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > SPAWN_INTERVAL:
        obstacle_x = SCREEN_WIDTH
        obstacle_y = SCREEN_HEIGHT - obstacle_height
        obstacles.append((obstacle_x, obstacle_y))
        last_spawn_time = current_time

    for i, (obstacle_x, obstacle_y) in enumerate(obstacles):
        obstacle_x -= obstacle_speed
        obstacles[i] = (obstacle_x, obstacle_y)
        draw_obstacle(obstacle_x, obstacle_y)

        if (player_x < obstacle_x + obstacle_width and
                player_x + player_size > obstacle_x and
                player_y + player_size > obstacle_y):
            print(f"Game Over! Final Score: {score}")
            pygame.quit()
            sys.exit()

        if obstacle_x < -obstacle_width:
            obstacles.pop(i)
            score += 1

    draw_player(player_x, player_y)
    display_score(score)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
