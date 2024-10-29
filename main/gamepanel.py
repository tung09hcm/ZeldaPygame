# gamepanel.py
import pygame
from entity.player import Player
class GamePanel:
    def __init__(self, width=992, height=624, title="My Pygame Window"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.background_color = (0, 0, 0)  # Đặt màu nền là đen
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.running = True
        self.player = Player()

    def run(self):
        while self.running:
            # Kiểm tra sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # Fill the background color
            self.window.fill(self.background_color)

            # Update the player animation and draw the player
            self.player.update_animation()
            self.player.draw(self.window)

            # Cập nhật màn hình
            pygame.display.flip()

        pygame.quit()
