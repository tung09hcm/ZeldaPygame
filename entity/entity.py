class Entity:
    def __init__(self):
        # Tọa độ trong thế giới
        self.worldX = 0
        self.worldY = 0
        self.speed = 0

        # Hình ảnh của các hướng di chuyển

        self.image = None
        # Hướng di chuyển hiện tại
        self.direction = ""

        # Các biến liên quan đến sprite
        self.spriteCounter = 0
        self.spriteNum = 1

        self.CollisionOn = False
