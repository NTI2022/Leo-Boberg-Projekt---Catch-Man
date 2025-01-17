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
    score_text = font.render(text, True, color)
    screen.blit(score_text, (x, y))


def main():
    #Starta
    screen, WIDTH, HEIGHT = initialize_game()

    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Spelare och objektinställningar
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

    #loop
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Hantera händelser
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

       
        
        object_y += object_speed

      

        # Kontrollera träff
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        object_rect = pygame.Rect(object_x, object_y, object_width, object_height)
        if player_rect.colliderect(object_rect):
            print("Game Over!")
            running = False

        # Spelaren och objektet
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, RED, object_rect)

        # Poängvisare
        draw_text(screen, f"Score: {score}", font, BLACK, 10, 10)

        # Uppdatera
        pygame.display.flip()

        
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()