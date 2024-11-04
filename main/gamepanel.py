import pygame
from entity.player import Player
from entity.goblin import Goblin
from entity.goblinKing import GoblinKing
import json
import time
import math

class GamePanel:
    def __init__(self, width=21 * 64, height=11 * 64, title="My Pygame Window"):
        pygame.init()
        self.defeat_boss = False
        self.spawn = True
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

        try:
            with open("setting.json", "r") as file:
                data = json.load(file)
                self.spawn = data.get("spawn")  # Default to "starter" if missing
                self.defeat_boss = data.get("defeat_boss")
        except FileNotFoundError:
            print(f"Không tìm thấy file player_data.json, sử dụng giá trị mặc định.")

        # Create an empty list to store the goblins
        self.goblins = []
        self.load_goblin_data()

        # Camera offset initialized to (0,0)
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.goblinKing = GoblinKing(self.map)

    def save_goblin_data(self):
        if self.player.player_save_game:
            xdata = {
                "spawn": self.spawn,
                "defeat_boss": self.defeat_boss
            }
            goblin_data_list = []
            for goblin in self.goblins:
                data = {
                    "level": goblin.level,
                    "max_hp": goblin.max_hp,
                    "current_hp": goblin.current_hp,
                    "exp": goblin.exp,
                    "money": goblin.money,
                    "worldX": goblin.worldX,
                    "worldY": goblin.worldY,
                    "speed": goblin.speed,
                    "attack_power": goblin.attack_power,
                    "defense": goblin.defense,
                    "direction": goblin.direction,
                    "state": goblin.state,
                }
                goblin_data_list.append(data)

            # Ghi dữ liệu vào file JSON
            with open("goblin_data.json", "w") as file:
                json.dump(goblin_data_list, file, indent=4)
            with open("setting.json", "w") as file:
                json.dump(xdata, file, indent=4)

    def load_goblin_data(self):
        try:
            # Đọc dữ liệu từ file JSON
            with open("goblin_data.json", "r") as file:
                goblin_data_list = json.load(file)
            if not goblin_data_list and self.player.current_map == "cave":
                print("File JSON rỗng. Khởi tạo 15 goblin mới.")
                if self.spawn:
                    for _ in range(15):
                        goblin = Goblin(self.map)
                        self.goblins.append(goblin)
                self.spawn = False
                return
            else:
                # Khôi phục từng goblin từ dữ liệu trong file
                self.goblins = []  # Khởi tạo lại danh sách goblin
                for data in goblin_data_list:
                    goblin = Goblin(self.map)
                    goblin.level = data["level"]
                    goblin.max_hp = data["max_hp"]
                    goblin.current_hp = data["current_hp"]
                    goblin.exp = data["exp"]
                    goblin.money = data["money"]
                    goblin.worldX = data["worldX"]
                    goblin.worldY = data["worldY"]
                    goblin.speed = data["speed"]
                    goblin.attack_power = data["attack_power"]
                    goblin.defense = data["defense"]
                    goblin.direction = data["direction"]
                    goblin.state = data["state"]

                    self.goblins.append(goblin)  # Thêm goblin mới vào danh sách

        except FileNotFoundError:
            print("File goblin_data.json không tồn tại.")
            if self.player.current_map == "cave":
                for _ in range(15):
                    goblin = Goblin(self.map)
                    self.goblins.append(goblin)
                self.spawn = False
        except json.JSONDecodeError:
            print("Lỗi đọc file goblin_data.json.")

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

    def playerLevelUp(self, goblin):
        self.player.current_xp += goblin.exp
        if self.player.current_xp > self.player.max_xp:
            self.player.level = self.player.level + 1
            self.player.max_hp += 8
            self.player.current_hp += 8
            self.player.current_xp = self.player.current_xp - self.player.max_xp
            self.player.max_xp += 30
            self.player.money += goblin.money
            self.player.attack_power += 7
            self.player.defense += 7

    def run(self):
        clock = pygame.time.Clock()
        attack_cooldown = 1.0

        while self.running:

            if self.player.current_hp == 0:
                self.intialize_map("../resources/map/starter")
                self.player.go_back_to_health_station()
                self.player.map = self.map
                self.spawn = True
                self.current_map = "starter"
            elif self.player.respawn:
                self.intialize_map("../resources/map/starter")
                self.player.respawn = False
                self.player.map = self.map
                self.spawn = True
                self.current_map = "starter"
                print("Goblin spawn lại")
            # if self.player.current_map == "starter":
            #     self.goblinKing = GoblinKing(self.map)
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
            # print("spawn: " + str(self.spawn))
            # print("player_current_map: " + str(self.player.current_map))
            if self.spawn and self.player.current_map == "cave":
                for _ in range(15):
                    goblin = Goblin(self.map)
                    self.goblins.append(goblin)
                    self.spawn = False
            for goblin in self.goblins:
                if not self.player.show_inventory:
                    if not goblin.update(self.window, self.camera_offset_x, self.camera_offset_y, self.player.worldX,
                                         self.player.worldY):
                        print("Xóa goblin")
                        self.goblins.remove(goblin)

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
                    sword_hit_box = pygame.Rect(self.player.worldX - 96 + self.camera_offset_x,
                                                self.player.worldY + self.camera_offset_y, 96, 96)
                    if self.player.direction == "left":
                        # print("left")
                        sword_hit_box = pygame.Rect(self.player.worldX - 96 + + self.camera_offset_x,
                                                    self.player.worldY + self.camera_offset_y, 96, 96)
                    elif self.player.direction == "right":
                        # print("right")
                        sword_hit_box = pygame.Rect(self.player.worldX + 64 + self.camera_offset_x,
                                                    self.player.worldY + self.camera_offset_y, 96, 96)
                    elif self.player.direction == "down":
                        # print("down")
                        sword_hit_box = pygame.Rect(self.player.worldX + self.camera_offset_x,
                                                    self.player.worldY + 96 + self.camera_offset_y, 64, 96)
                    elif self.player.direction == "up":
                        # print("up")
                        sword_hit_box = pygame.Rect(self.player.worldX + self.camera_offset_x,
                                                    self.player.worldY - 96 + self.camera_offset_y, 64, 96)

                    # Vẽ viền màu trắng quanh sword_hit_box
                    pygame.draw.rect(self.window, (255, 255, 255), sword_hit_box, 3)
                    goblin_hit_box = pygame.Rect(goblin.worldX + 32 + self.camera_offset_x,
                                                 goblin.worldY + 32 + self.camera_offset_y, 64, 64)
                    pygame.draw.rect(self.window, (255, 255, 255), goblin_hit_box, 3)
                    if goblin_hit_box.colliderect(sword_hit_box):
                        damage = (self.player.attack_power - goblin.defense) if (
                                                                                        self.player.attack_power - goblin.defense) > 0 else 3

                        goblin.current_hp -= damage
                        if goblin.current_hp <= 0:
                            goblin.current_hp = 0
                            goblin.state = "death"
                            self.playerLevelUp(goblin)
            # BOSS
            if len(self.goblins) == 0 and self.player.current_map == "cave" and not self.defeat_boss:

                if self.goblinKing.current_hp == 0:
                    self.goblinKing.state = "death"
                    self.defeat_boss = True
                if not self.player.show_inventory:
                    if self.goblinKing.update(self.window, self.camera_offset_x, self.camera_offset_y,
                                           self.player.worldX,
                                           self.player.worldY):
                        print("goblinKing state: " + self.goblinKing.state)
                        distance = math.sqrt((self.player.worldX - self.goblinKing.worldX + 64 * 4) ** 2 + (self.player.worldY - self.goblinKing.worldY + 64 * 4) ** 2)
                        if self.goblinKing.state == "attack" and distance < 64:
                            print("Goblin King ATTACk")
                            current_time = time.time()
                            if current_time - self.goblinKing.last_attack_time >= 0.5:
                                # Apply damage to the player
                                damage = (self.goblinKing.attack_power - self.player.defense) if (
                                                                                                             self.goblinKing.attack_power - self.player.defense) > 0 else 20

                                self.player.current_hp -= damage
                                if self.player.current_hp <= 0:
                                    self.player.current_hp = 0
                                # Update the last attack time for the goblin
                                self.goblinKing.last_attack_time = current_time
                        else:
                            self.goblinKing.state = "move"
                # check goblin có nằm trong tầm đánh của player ko
                if self.player.attack and self.goblinKing.state != "death":
                    sword_hit_box = pygame.Rect(self.player.worldX - 96 + self.camera_offset_x,
                                                self.player.worldY + self.camera_offset_y, 96, 96)
                    if self.player.direction == "left":
                        # print("left")
                        sword_hit_box = pygame.Rect(self.player.worldX - 96 + + self.camera_offset_x,
                                                    self.player.worldY + self.camera_offset_y, 96, 96)
                    elif self.player.direction == "right":
                        # print("right")
                        sword_hit_box = pygame.Rect(self.player.worldX + 64 + self.camera_offset_x,
                                                    self.player.worldY + self.camera_offset_y, 96, 96)
                    elif self.player.direction == "down":
                        # print("down")
                        sword_hit_box = pygame.Rect(self.player.worldX + self.camera_offset_x,
                                                    self.player.worldY + 96 + self.camera_offset_y, 64, 96)
                    elif self.player.direction == "up":
                        # print("up")
                        sword_hit_box = pygame.Rect(self.player.worldX + self.camera_offset_x,
                                                    self.player.worldY - 96 + self.camera_offset_y, 64, 96)

                    # Vẽ viền màu trắng quanh sword_hit_box
                    pygame.draw.rect(self.window, (255, 255, 255), sword_hit_box, 3)
                    goblin_hit_box = pygame.Rect(self.goblinKing.worldX + 64 * 2 + self.camera_offset_x,
                                                 self.goblinKing.worldY + 64 * 2 + self.camera_offset_y, 64 * 4, 64 * 4)
                    pygame.draw.rect(self.window, (255, 255, 255), goblin_hit_box, 3)
                    if goblin_hit_box.colliderect(sword_hit_box):
                        damage = (self.player.attack_power - self.goblinKing.defense) if (
                                                                                                     self.player.attack_power - self.goblinKing.defense) > 0 else 10

                        self.goblinKing.current_hp -= damage
                        if self.goblinKing.current_hp <= 0:
                            self.goblinKing.current_hp = 0
                            self.goblinKing.state = "death"
                            self.playerLevelUp(self.goblinKing)

            self.checkPlayerAttack()
            self.player.attack = False
            self.save_goblin_data()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
