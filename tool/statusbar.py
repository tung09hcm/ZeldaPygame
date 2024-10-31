import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("HP and XP Bars")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)

# Font
font = pygame.font.Font(None, 36)

# HP and XP values
max_hp = 296
current_hp = 296
max_xp = 100
current_xp = 100  # Example value for XP


# Function to draw bars
def draw_bars():
    # Draw background
    screen.fill(DARK_GRAY)

    # Draw HP bar outline with rounded corners
    pygame.draw.rect(screen, WHITE, (50, 50, 200, 20), 2, border_radius=5)
    # Calculate HP bar width
    hp_width = int((current_hp / max_hp) * 198)  # Leave some margin for outline
    # Draw HP bar with rounded corners
    pygame.draw.rect(screen, GREEN, (51, 51, hp_width, 18))

    # Draw XP bar outline with rounded corners
    pygame.draw.rect(screen, WHITE, (50, 80, 200, 10), 2, border_radius=5)
    # Calculate XP bar width
    xp_width = int((current_xp / max_xp) * 198)  # Leave some margin for outline
    # Draw XP bar with rounded corners
    pygame.draw.rect(screen, BLUE, (51, 81, xp_width, 8))

    # Display HP text
    hp_text = font.render(f"HP: {current_hp}/{max_hp}", True, WHITE)
    screen.blit(hp_text, (50, 20))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_bars()

    pygame.display.flip()

pygame.quit()
