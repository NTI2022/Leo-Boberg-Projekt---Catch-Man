import pygame
import random
import sys

def initialize_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Catch Man")
    return screen, WIDTH, HEIGHT

def draw_text(screen, text, font, color, x, y):
    score_text = font.render(text, True, color)
    screen.blit(score_text, (x, y))

def player_movement(keys, player_x, player_speed, WIDTH, player_width):
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    return player_x

def reset_object(object_y, HEIGHT, object_height, WIDTH, object_width):
    if object_y > HEIGHT:
        object_y = -object_height
        object_x = random.randint(0, WIDTH - object_width)
        return object_x, object_y, True
    return None, object_y, False

def main():
    
    screen, WIDTH, HEIGHT = initialize_game()

    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    player_width, player_height = 50, 50
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 10

    object_width, object_height = 30, 30
    object_x = random.randint(0, WIDTH - object_width)
    object_y = -object_height
    object_speed = 5

    score = 0
    font = pygame.font.Font(None, 36)

    
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_x = player_movement(keys, player_x, player_speed, WIDTH, player_width)

        object_y += object_speed

        object_x_reset, object_y, scored = reset_object(object_y, HEIGHT, object_height, WIDTH, object_width)
        if scored:
            object_x = object_x_reset
            score += 1

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        object_rect = pygame.Rect(object_x, object_y, object_width, object_height)
        if player_rect.colliderect(object_rect):
            print("Game Over!")
            running = False

        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, RED, object_rect)

        draw_text(screen, f"Score: {score}", font, BLACK, 10, 10)

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()