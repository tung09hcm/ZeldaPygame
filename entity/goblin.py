from entity.entity import Entity
import pygame
import os
import json
import random

class Goblin(Entity):
    def __init__(self, game_map):
        super().__init__()
        self.worldX = random.randint(16, 30) * 64
        self.worldY = random.randint(4, 16) * 64
        self.level = random.randint(1, 3)
        self.max_hp = random.randint(25, 30)
        self.current_hp = self.max_hp
        self.xp = random.randint(10, 15)
        self.money = random.randint(10, 20)
        self.direction = "down"

        self.speed = 7
        self.attack_power = 10
        self.defense = 5
        self.map = game_map
        # Initialize animation
        self.current_frame = 0
        self.animation_counter = 0  # To control animation speed

        self.down_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/000.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/031.png").convert_alpha())
        ]
        self.left_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/004.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/009.png").convert_alpha())
        ]
        self.right_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/010.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/016.png").convert_alpha())
        ]
        self.up_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/003.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/032.png").convert_alpha())
        ]

        self.attack_down_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/001.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/030.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/023.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/015.png").convert_alpha())
        ]
        self.attack_left_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/005.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/006.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/007.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/008.png").convert_alpha())
        ]
        self.attack_right_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/011.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/012.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/013.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/014.png").convert_alpha())
        ]
        self.attack_up_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/002.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/033.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/034.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/035.png").convert_alpha())
        ]

        self.hurt_down_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/017.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/018.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/019.png").convert_alpha())
        ]
        self.hurt_up_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/020.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/021.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/022.png").convert_alpha())
        ]
        self.hurt_left_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/024.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/025.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/026.png").convert_alpha())
        ]
        self.hurt_right_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/027.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/028.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/029.png").convert_alpha())
        ]
