import pygame

class Tile:
    def __init__(self, image_path, collision=False):
        # Tải ảnh của tile từ đường dẫn
        self.image = pygame.transform.scale2x(pygame.image.load(image_path).convert_alpha())
        self.collision = collision
