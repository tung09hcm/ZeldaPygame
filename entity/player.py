from entity.entity import Entity
import pygame


class Player(Entity):
    def __init__(self):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha (Entity)
        self.worldX = 496-32
        self.worldY = 312-48
        # Các biến riêng cho Player
        self.speed = 5
        self.health = 100  # Ví dụ: sức khỏe của người chơi
        self.attack_power = 10  # Ví dụ: sức tấn công của người chơi
        self.defense = 5  # Ví dụ: sức phòng thủ của người chơi
        self.direction = "down"
        # Load images for different animations
        self.down_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/player/1.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/2.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/3.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/4.png").convert_alpha())
        ]
        self.left_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/player/5.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/6.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/7.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/8.png").convert_alpha())
        ]
        self.right_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/player/9.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/10.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/11.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/12.png").convert_alpha())
        ]
        self.up_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/player/13.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/14.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/15.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/player/16.png").convert_alpha())
        ]

        # Initialize animation
        self.current_frame = 0
        self.animation_counter = 0  # To control animation speed

    def update_animation(self):
        # Switch frame every 10 game ticks
        self.animation_counter += 1
        if self.animation_counter % 10 == 0:
            self.current_frame = (self.current_frame + 1) % 4

    def draw(self, screen):
        # Select the correct animation based on direction
        if self.direction == "up":
            self.image = self.up_images[self.current_frame]
        elif self.direction == "down":
            self.image = self.down_images[self.current_frame]
        elif self.direction == "left":
            self.image = self.left_images[self.current_frame]
        elif self.direction == "right":
            self.image = self.right_images[self.current_frame]

        # Draw the player on the screen at the current position
        screen.blit(self.image, (self.worldX, self.worldY))
