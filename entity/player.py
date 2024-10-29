from entity.entity import Entity
import pygame


class Player(Entity):
    def __init__(self):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha (Entity)
        self.worldX = 496 - 32
        self.worldY = 312 - 48
        # Các biến riêng cho Player
        self.speed = 7
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
        self.click = False
        self.attack = False
        self.attack_up = pygame.image.load("../resources/player/sword_up.png").convert_alpha()
        self.attack_down = pygame.image.load("../resources/player/sword_down.png").convert_alpha()
        self.attack_right = pygame.image.load("../resources/player/sword_right.png").convert_alpha()
        self.attack_left = pygame.image.load("../resources/player/sword_left.png").convert_alpha()

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.attack = True
            self.speed = 3
        if keys[pygame.K_UP]:
            self.worldY -= self.speed
            self.direction = "up"
            self.click = True
        elif keys[pygame.K_DOWN]:
            self.worldY += self.speed
            self.direction = "down"
            self.click = True
        elif keys[pygame.K_LEFT]:
            self.worldX -= self.speed
            self.direction = "left"
            self.click = True
        elif keys[pygame.K_RIGHT]:
            self.worldX += self.speed
            self.direction = "right"
            self.click = True

    def update_animation(self):
        # Switch frame every 10 game ticks
        self.animation_counter += 1
        if not self.click:
            if self.direction == "down":
                self.image = self.down_images[3]
            if self.direction == "left":
                self.image = self.left_images[3]
            if self.direction == "right":
                self.image = self.right_images[3]
            if self.direction == "up":
                self.image = self.up_images[3]
            return
        if self.animation_counter % 10 == 0:
            self.current_frame = (self.current_frame + 1) % 4
        self.click = False

    def draw(self, screen):
        # Select the correct animation based on direction
        if not self.click:
            if self.direction == "down":
                self.image = self.down_images[3]
            if self.direction == "left":
                self.image = self.left_images[3]
            if self.direction == "right":
                self.image = self.right_images[3]
            if self.direction == "up":
                self.image = self.up_images[3]
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
        if self.attack:
            if self.direction == "up":
                screen.blit(self.attack_up, (self.worldX + 8, self.worldY - 40))
            elif self.direction == "down":
                screen.blit(self.attack_down, (self.worldX + 8, self.worldY + 96))
            elif self.direction == "left":
                screen.blit(self.attack_left, (self.worldX - 48, self.worldY + 32))
            elif self.direction == "right":
                screen.blit(self.attack_right, (self.worldX + 48 + 13, self.worldY + 32))
            self.attack = False
            self.speed = 7
