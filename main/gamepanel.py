import pygame
from entity.player import Player
from entity.goblin import Goblin
import json
import time


class GamePanel:
    def __init__(self, width=21 * 64, height=11 * 64, title="My Pygame Window"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.background_color = (0, 0, 0)  # Background color set to black
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.running = True

        self.tile_size = 64

        # Load title images
        self.title = []
        for i in range(903):
            filename = f"../resources/pokemon_directory/{i:03}.png"
            image = pygame.image.load(filename).convert_alpha()
            scaled_image = (pygame.transform.scale2x(image))  # Scale the image 4x
            self.title.append(scaled_image)

        # Load map from file
        self.map = []
        self.intialize_map("../resources/map/starter")
        self.player = Player(self.map)

        try:
            with open("player_data.json", "r") as file:
                data = json.load(file)
                self.current_map = data.get("current_map")  # Default to "starter" if missing
                self.intialize_map(f"../resources/map/{self.current_map}")
                self.player.set_map(self.map)
        except FileNotFoundError:
            print(f"Không tìm thấy file player_data.json, sử dụng giá trị mặc định.")

        # Create an empty list to store the goblins
        self.goblins = []

        # Assuming `game_map` is already initialized in your main game code
        for _ in range(1):
            goblin = Goblin(self.map)
            self.goblins.append(goblin)

        # Camera offset initialized to (0,0)
        self.camera_offset_x = 0
        self.camera_offset_y = 0

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if not self.player.show_inventory:
            if keys[pygame.K_j]:
                self.player.attack = True
                self.player.speed = 7

    def intialize_map(self, file_map):
        self.map = []
        with open(file_map, 'r') as file:
            for line in file:
                row = [int(value) for value in line.split()]
                self.map.append(row)

    def update_camera(self):
        """Update the camera offset based on the player's position."""
        # Center the camera on the player, with a margin around the player for movement
        screen_center_x = self.width // 2
        screen_center_y = self.height // 2

        # Calculate the camera offset so the player stays near the center of the screen
        self.camera_offset_x = self.player.worldX - screen_center_x
        self.camera_offset_y = self.player.worldY - screen_center_y

    def calculate_camera_offset(self):
        """Calculate the camera offset to keep the player near the center of the screen."""
        # Keep the player roughly centered
        screen_center_x = self.width // 2
        screen_center_y = self.height // 2
        self.camera_offset_x = screen_center_x - self.player.worldX
        self.camera_offset_y = screen_center_y - self.player.worldY

    def draw_map(self):
        """Draws the map on the screen using the images in self.title with camera offset."""
        for row_index, row in enumerate(self.map):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size + self.camera_offset_x
                y = row_index * self.tile_size + self.camera_offset_y

                if 0 <= tile < len(self.title):
                    tile_image = self.title[tile]
                    self.window.blit(tile_image, (x, y))

    def checkPlayerAttack(self):
        # Calculate on-screen position
        screen_x = self.player.worldX + self.camera_offset_x
        screen_y = self.player.worldY + self.camera_offset_y
        if self.player.attack:
            if self.player.direction == "up":
                self.window.blit(self.player.attack_up, (screen_x, screen_y - 64))
            elif self.player.direction == "down":
                self.window.blit(self.player.attack_down, (screen_x, screen_y + 64))
            elif self.player.direction == "left":
                self.window.blit(self.player.attack_left, (screen_x - 64, screen_y))
            elif self.player.direction == "right":
                self.window.blit(self.player.attack_right, (screen_x + 64, screen_y))
            # self.player.attack = False
            self.player.speed = 12
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        clock = pygame.time.Clock()
        attack_cooldown = 1.0
        while self.running:
            self.handle_keys()

            self.calculate_camera_offset()

            self.window.fill(self.background_color)
            self.draw_map()

            # Kiểm tra nếu người chơi thoát khỏi mart/cave về overworld
            tilex = self.player.worldX // self.tile_size
            tiley = self.player.worldY // self.tile_size

            if tilex == 16 and tiley == 18 and not self.player.overWorld and self.player.current_map == "mart":
                self.player.current_map = "starter"
                # Hiển thị màn hình đen tạm thời trong 50ms
                self.window.fill((0, 0, 0))
                pygame.display.flip()
                pygame.time.delay(50)

                self.intialize_map("../resources/map/starter")
                self.player.set_map(self.map)
                self.player.worldX = 11 * 64
                self.player.worldY = 16 * 64
                self.player.overWorld = True
                self.player.Mart = False
                self.player.Cave = False
                print("Enter the Overworld")
            if (
                    tilex == 23 or tilex == 22) and tiley == 29 and not self.player.overWorld and self.player.current_map == "cave":
                print("gán map thành starter")
                self.player.current_map = "starter"
                # Hiển thị màn hình đen tạm thời trong 50ms
                self.window.fill((0, 0, 0))
                pygame.display.flip()
                pygame.time.delay(50)

                self.intialize_map("../resources/map/starter")
                self.player.set_map(self.map)
                self.player.worldX = 16 * 64
                self.player.worldY = 43 * 64
                self.player.overWorld = True
                self.player.Mart = False
                self.player.Cave = False
                print("Enter the Overworld")

            # Draw player with camera offset
            self.player.handle_keys()
            self.player.update_animation()
            self.player.draw(self.window, self.camera_offset_x, self.camera_offset_y)
            self.player.checkgomart()

            # Kiểm tra sự kiện chuyển bản đồ khi vào mart
            if self.player.Mart:
                self.player.current_map = "mart"
                # Hiển thị màn hình đen tạm thời trong 50ms
                self.window.fill((0, 0, 0))
                pygame.display.flip()
                pygame.time.delay(50)

                self.intialize_map("../resources/map/mart")
                self.player.set_map(self.map)  # Cập nhật bản đồ cho đối tượng Player
                self.player.worldX = 16 * 64  # Đặt lại tọa độ x cho người chơi trong mart
                self.player.worldY = 17 * 64  # Đặt lại tọa độ y cho người chơi trong mart
                self.player.Mart = False  # Đặt lại Mart thành False để không lặp lại sự kiện
            # Kiểm tra sự kiện chuyển bản đồ khi vào cave
            elif self.player.Cave:
                self.player.current_map = "cave"
                # Hiển thị màn hình đen tạm thời trong 50ms
                self.window.fill((0, 0, 0))
                pygame.display.flip()
                pygame.time.delay(50)

                self.intialize_map("../resources/map/cave")
                self.player.set_map(self.map)  # Cập nhật bản đồ cho đối tượng Player
                self.player.worldX = 23 * 64  # Đặt lại tọa độ x cho người chơi trong cave
                self.player.worldY = 28 * 64  # Đặt lại tọa độ y cho người chơi trong cave
                self.player.Cave = False  # Đặt lại Mart thành False để không lặp lại sự kiện

            for goblin in self.goblins:
                if not self.player.show_inventory:
                    goblin.update(self.window, self.camera_offset_x, self.camera_offset_y, self.player.worldX,
                                  self.player.worldY)
                    goblin.check_collision_with_other_goblins(self.goblins)
                    if goblin.state == "attack":
                        current_time = time.time()
                        if current_time - goblin.last_attack_time >= attack_cooldown:
                            # Apply damage to the player
                            damage = (goblin.attack_power - self.player.defense) if (
                                                                                            goblin.attack_power - self.player.defense) > 0 else 3
                            self.player.current_hp -= damage
                            if self.player.current_hp <= 0:
                                self.player.current_hp = 0
                            # Update the last attack time for the goblin
                            goblin.last_attack_time = current_time
                # check goblin có nằm trong tầm đánh của player ko
                if self.player.attack:
                    if self.player.direction == "left":
                        print(1)
                        sword_hit_box = pygame.Rect(self.player.worldX - 96, self.player.worldY, 96, 96)
                        if goblin.hitbox.colliderect(sword_hit_box):
                            print(2)

                    elif self.player.direction == "right":
                        print(1)
                        sword_hit_box = pygame.Rect(self.player.worldX + 96, self.player.worldY, 96, 96)
                    elif self.player.direction == "down":
                        print(1)
                        sword_hit_box = pygame.Rect(self.player.worldX, self.player.worldY+96, 64, 96)
                    elif self.player.direction == "up":
                        print(1)
                        sword_hit_box = pygame.Rect(self.player.worldX, self.player.worldY-96, 64, 96)

            self.checkPlayerAttack()
            self.player.attack = False
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
