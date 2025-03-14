"""__author__  = "Leo Boberg"
__version__ = "1.0.0"
__email__   = "leo.boberg@elev.ga.ntig.se"""

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
    # Ritar text på skärmen
    score_text = font.render(text, True, color)
    screen.blit(score_text, (x, y))

def player_movement(keys, player_x, player_speed, WIDTH, player_width):
    # Hanterar spelarens rörelse
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    return player_x

def reset_object(object_y, HEIGHT, object_height, WIDTH, object_width):
    # Återställer föremålet om det åker utanför skärmen
    if object_y > HEIGHT:
        object_y = -object_height
        object_x = random.randint(0, WIDTH - object_width)
        return object_x, object_y, True
    return None, object_y, False

def main():
    screen, WIDTH, HEIGHT = initialize_game()

    # Färger
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Spelarens egenskaper
    player_width, player_height = 50, 20
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 30

    # Föremålets egenskaper
    object_width, object_height = 30, 30
    object_x = random.randint(0, WIDTH - object_width)
    object_y = -object_height
    object_speed = 5
    speed_increment = 0.5  # Ökning av hastighet per poäng

    is_green = random.choice([True, False])

    score = 0
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Hantera händelser
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Hantera spelarens rörelse
        keys = pygame.key.get_pressed()
        player_x = player_movement(keys, player_x, player_speed, WIDTH, player_width)

        # Uppdatera föremålets position
        object_y += object_speed
        object_x_reset, object_y, scored = reset_object(object_y, HEIGHT, object_height, WIDTH, object_width)
        if scored:
            object_x = object_x_reset
            is_green = random.choice([True, False])

        # Kollisionsdetektion
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        object_rect = pygame.Rect(object_x, object_y, object_width, object_height)
        
        if player_rect.colliderect(object_rect):
            if is_green:
                score += 1
                object_speed += speed_increment  # Öka hastigheten när spelaren får poäng
                object_x, object_y = reset_object(HEIGHT, HEIGHT, object_height, WIDTH, object_width)[:2]
            else:
                print("Game Over!")
                running = False

        # Rita spelaren och föremålet
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, GREEN if is_green else RED, object_rect)

        # Visa poängen på skärmen
        draw_text(screen, f"Poäng: {score}", font, BLACK, 10, 10)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()