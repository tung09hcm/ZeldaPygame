class Entity:
    def __init__(self):
        # Tọa độ trong thế giới
        self.worldX = 0
        self.worldY = 0
        self.speed = 0

        # Hình ảnh của các hướng di chuyển
        self.up1 = None
        self.up2 = None
        self.down1 = None
        self.down2 = None
        self.left1 = None
        self.left2 = None
        self.right1 = None
        self.right2 = None
        self.up3 = None
        self.up4 = None
        self.down3 = None
        self.down4 = None
        self.left3 = None
        self.left4 = None
        self.right3 = None
        self.right4 = None
        self.image = None
        # Hướng di chuyển hiện tại
        self.direction = ""

        # Các biến liên quan đến sprite
        self.spriteCounter = 0
        self.spriteNum = 1

        self.CollisionOn = False
