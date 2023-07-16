import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load the background image
background_image = pygame.image.load("istockphoto-1035676256-612x612.jpg")
background_rect = background_image.get_rect()

# Set up colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the player
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 8
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Set up the enemies
num_enemies = 5
enemy_width = 50
enemy_height = 50
enemies = []
for _ in range(num_enemies):
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
    enemy_y = random.randint(50, 200)
    enemy_speed_x = random.uniform(-1, 1)  # Horizontal speed
    enemy_speed_y = random.uniform(0.1, 1.5)  # Vertical speed
    enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemies.append((enemy, enemy_speed_x, enemy_speed_y))

# Set up bullets
bullet_width = 5
bullet_height = 15
bullet_speed = 10
bullet_max_quantity = 5
bullets = []
bullet_state = "ready"

# Set up the score
score_value = 0
font = pygame.font.Font(None, 36)

# Function to display the score on the screen
def show_score():
    score_text = font.render("Score: " + str(score_value), True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to draw bullets on the screen
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

# Function to draw enemies on the screen
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy[0])

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Limit the frame rate to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < bullet_max_quantity:
            bullet = pygame.Rect(player.x + player_width // 2 - bullet_width // 2, player.y, bullet_width, bullet_height)
            bullets.append(bullet)

    # Update the player's position
    player.left = max(player.left, 0)
    player.right = min(player.right, SCREEN_WIDTH)

    # Update the enemies' positions
    updated_enemies = []
    for enemy in enemies:
        enemy_rect, enemy_speed_x, enemy_speed_y = enemy
        enemy_rect.y += enemy_speed_y
        enemy_rect.x += enemy_speed_x

        if enemy_rect.top > SCREEN_HEIGHT or enemy_rect.left < 0 or enemy_rect.right > SCREEN_WIDTH:
            enemy_speed_x = random.uniform(-1, 1)
            enemy_rect.y = random.randint(50, 200)

        if enemy_rect.bottom >= SCREEN_HEIGHT:
            running = False

        updated_enemies.append((enemy_rect, enemy_speed_x, enemy_speed_y))
    enemies = updated_enemies

    # Update the bullets' positions
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Check for collision between the bullets and the enemies
    for bullet in bullets:
        for enemy in enemies:
            enemy_rect, _, _ = enemy
            if bullet.colliderect(enemy_rect):
                enemy_rect.x = random.randint(0, SCREEN_WIDTH - enemy_width)
                enemy_rect.y = random.randint(50, 200)
                bullets.remove(bullet)
                score_value += 1

    # Draw the background image
    screen.blit(background_image, background_rect)

    # Draw the player, enemies, bullets, and score on the screen
    pygame.draw.rect(screen, GREEN, player)
    draw_enemies()
    draw_bullets()
    show_score()

    # Update the display
    pygame.display.update()

# Show final score
final_score_text = font.render("Final Score: " + str(score_value), True, WHITE)
screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - final_score_text.get_height() // 2))
pygame.display.update()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit the game
pygame.quit()
