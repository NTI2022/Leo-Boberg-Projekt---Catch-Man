"""""
Game.py: Huvudfilen för spelet

__author__  = "Leo Boberg"
__version__ = "1.6.0"
__email__   = "leo.boberg@elev.ga.ntig.se"
"""

import pygame  
import random  
import sys     # För att kunna avsluta spelet

# Funktion för att läsa in highscore från en fil
# Om filen inte finns, returnerar vi 0

def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Funktion för att spara highscore till en fil
def save_highscore(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# Startar spelet och sätter upp fönstret
def initialize_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Catch Man")
    return screen, WIDTH, HEIGHT

# Funktion för att rita text på skärmen
def draw_text(screen, text, font, color, x, y):
    score_text = font.render(text, True, color)
    screen.blit(score_text, (x, y))

# Hanterar spelarens rörelser baserat på knapptryckningar
def player_movement(keys, player_x, player_speed, WIDTH, player_width):
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    return player_x

# Återställer objektets position om det fallit utanför skärmen
def reset_object(object_y, HEIGHT, object_height, WIDTH, object_width):
    if object_y > HEIGHT:
        object_y = -object_height  # Startar om ovanför skärmen
        object_x = random.randint(0, WIDTH - object_width)  # Ny slumpmässig position
        return object_x, object_y, True  # Objektet har återställts
    return None, object_y, False

# Visar startmenyn innan spelet börjar
def show_start_menu(screen, font, WIDTH, HEIGHT):
    screen.fill((255, 255, 255))  # Bakgrundsfärg
    draw_text(screen, "Välkommen till Catch Man!", font, (0, 0, 0), WIDTH // 2 - 150, HEIGHT // 3)
    draw_text(screen, "Tryck på ENTER för att börja", font, (0, 0, 0), WIDTH // 2 - 150, HEIGHT // 2)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False  # Starta spelet!

# Visar slutskärmen när spelet är över
def show_end_screen(screen, font, score, highscore, WIDTH, HEIGHT):
    screen.fill((255, 255, 255))
    if score > highscore:
        draw_text(screen, f"GRATTIS! Nytt highscore: {score}", font, (0, 255, 0), WIDTH // 2 - 200, HEIGHT // 3)
        save_highscore(score)
    else:
        draw_text(screen, f"Game over!", font, (255, 0, 0), WIDTH // 2 - 150, HEIGHT // 4)
        draw_text(screen, f"Du fick {score} poäng", font, (255, 0, 0), WIDTH // 2 - 150, HEIGHT // 3)
        draw_text(screen, f"Highscore: {highscore}", font, (0, 0, 0), WIDTH // 2 - 150, HEIGHT // 2)
    
    pygame.display.flip()
    pygame.time.wait(3000)  # Vänta 3 sek innan spelet avslutas
    pygame.quit()
    sys.exit()

# Huvudfunktionen för spelet
def main():
    screen, WIDTH, HEIGHT = initialize_game()
    
    # Definiera färger
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    highscore = load_highscore()  # Ladda highscore från fil
    
    # Spelarens egenskaper
    player_width, player_height = 90, 20
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 30
    
    # Objektets egenskaper
    object_width, object_height = 30, 30
    object_x = random.randint(0, WIDTH - object_width)
    object_y = -object_height
    object_speed = 5
    speed_increment = 0.5
    is_green = random.choice([True, False])
    
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    show_start_menu(screen, font, WIDTH, HEIGHT)  # Visa startmenyn
    
    running = True
    while running:
        screen.fill(WHITE)  # Rensa skärmen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        player_x = player_movement(keys, player_x, player_speed, WIDTH, player_width)
        
        object_y += object_speed
        object_x_reset, object_y, scored = reset_object(object_y, HEIGHT, object_height, WIDTH, object_width)
        if scored:
            object_x = object_x_reset
            is_green = random.choice([True, False])
        
        # Kollision mellan spelaren och objektet
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        object_rect = pygame.Rect(object_x, object_y, object_width, object_height)
        
        if player_rect.colliderect(object_rect):
            if is_green:
                score += 1
                object_speed += speed_increment
            else:
                lives -= 1
                if lives == 0:
                    show_end_screen(screen, font, score, highscore, WIDTH, HEIGHT)
                    running = False
            object_x, object_y = reset_object(HEIGHT, HEIGHT, object_height, WIDTH, object_width)[:2]
        
        # Rita spelaren och objektet
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, GREEN if is_green else RED, object_rect)
        
        # Rita poäng, highscore och liv på skärmen
        draw_text(screen, f"Poäng: {score}", font, BLACK, 10, 10)
        draw_text(screen, f"Highscore: {highscore}", font, BLACK, 10, 40)
        draw_text(screen, f"Liv: {lives}", font, BLACK, WIDTH - 100, 10)
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
