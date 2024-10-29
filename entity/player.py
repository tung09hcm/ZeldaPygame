from entity.entity import Entity
import pygame


class Player(Entity):
    def __init__(self):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha (Entity)

        # Các biến riêng cho Player
        self.speed = 5
        self.health = 100  # Ví dụ: sức khỏe của người chơi
        self.attack_power = 10  # Ví dụ: sức tấn công của người chơi
        self.defense = 5  # Ví dụ: sức phòng thủ của người chơi
        self.direction = "down"
        self.down1 = pygame.image.load("../resources/player/1.png").convert_alpha()
        self.down2 = pygame.image.load("../resources/player/2.png").convert_alpha()
        self.down3 = pygame.image.load("../resources/player/3.png").convert_alpha()
        self.down4 = pygame.image.load("../resources/player/4.png").convert_alpha()

        self.left1 = pygame.image.load("../resources/player/5.png").convert_alpha()
        self.left2 = pygame.image.load("../resources/player/6.png").convert_alpha()
        self.left3 = pygame.image.load("../resources/player/7.png").convert_alpha()
        self.left4 = pygame.image.load("../resources/player/8.png").convert_alpha()

        self.right1 = pygame.image.load("../resources/player/9.png").convert_alpha()
        self.right2 = pygame.image.load("../resources/player/10.png").convert_alpha()
        self.right3 = pygame.image.load("../resources/player/11.png").convert_alpha()
        self.right4 = pygame.image.load("../resources/player/12.png").convert_alpha()

        self.up1 = pygame.image.load("../resources/player/13.png").convert_alpha()
        self.up2 = pygame.image.load("../resources/player/14.png").convert_alpha()
        self.up3 = pygame.image.load("../resources/player/15.png").convert_alpha()
        self.up4 = pygame.image.load("../resources/player/16.png").convert_alpha()


    def draw(self):
        if self.direction == "up":
            self.image = self.up1
        elif self.direction == "down":
            self.image = self.down1
        elif self.direction == "left":
            self.image = self.left1
        elif self.direction == "right":
            self.image = self.right1

