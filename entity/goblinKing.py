from entity.entity import Entity
import pygame
import os
import json
import random
import math
import time


def load_scaled_image(path, scale_factor=8):
    image = pygame.image.load(path).convert_alpha()
    width, height = image.get_size()
    return pygame.transform.scale(image, (width * scale_factor, height * scale_factor))


class GoblinKing(Entity):
    def init_collison(self, filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()

            for i in range(0, len(lines), 2):  # Bước qua từng cặp dòng
                code = lines[i].strip()  # Mã
                is_blocked = lines[i + 1].strip()  # Giá trị true/false

                if is_blocked.lower() == 'true':  # Kiểm tra nếu là true
                    # Lấy số từ mã (giả sử mã có định dạng như '000.png')
                    number = int(code.split('.')[0])  # Lấy phần trước dấu '.'
                    self.blocked_code.append(number)  # Thêm số vào danh sách

    def __init__(self, game_map):
        super().__init__()
        self.last_attack_time = 0
        self.tile_size = 64
        self.blocked_code = []
        self.init_collison("../resources/map/collison")
        self.worldX = 23 * 64
        self.worldY = 10 * 64
        self.level = 15
        self.max_hp = 1500
        self.current_hp = self.max_hp
        self.exp = 100
        self.money = 1000
        self.direction = "down"
        self.state = "idle"  # Possible states: idle, attack, hurt, move
        self.speed = 3
        self.attack_power = 30
        self.defense = 30
        self.map = game_map
        self.current_frame = 0
        self.animation_counter = 0

        self.death_time = 0

        self.down_images = [
            load_scaled_image("../resources/goblin/000.png"),
            load_scaled_image("../resources/goblin/031.png")
        ]
        self.left_images = [
            load_scaled_image("../resources/goblin/004.png"),
            load_scaled_image("../resources/goblin/009.png")
        ]
        self.right_images = [
            load_scaled_image("../resources/goblin/010.png"),
            load_scaled_image("../resources/goblin/016.png")
        ]
        self.up_images = [
            load_scaled_image("../resources/goblin/003.png"),
            load_scaled_image("../resources/goblin/032.png")
        ]

        self.attack_down_images = [
            load_scaled_image("../resources/goblin/001.png"),
            load_scaled_image("../resources/goblin/030.png"),
            load_scaled_image("../resources/goblin/023.png"),
            load_scaled_image("../resources/goblin/015.png")
        ]
        self.attack_left_images = [
            load_scaled_image("../resources/goblin/005.png"),
            load_scaled_image("../resources/goblin/006.png"),
            load_scaled_image("../resources/goblin/007.png"),
            load_scaled_image("../resources/goblin/008.png")
        ]
        self.attack_right_images = [
            load_scaled_image("../resources/goblin/011.png"),
            load_scaled_image("../resources/goblin/012.png"),
            load_scaled_image("../resources/goblin/013.png"),
            load_scaled_image("../resources/goblin/014.png")
        ]
        self.attack_up_images = [
            load_scaled_image("../resources/goblin/002.png"),
            load_scaled_image("../resources/goblin/033.png"),
            load_scaled_image("../resources/goblin/034.png"),
            load_scaled_image("../resources/goblin/035.png")
        ]

        self.hurt_down_images = [
            load_scaled_image("../resources/goblin/017.png"),
            load_scaled_image("../resources/goblin/018.png"),
            load_scaled_image("../resources/goblin/019.png")
        ]
        self.hurt_up_images = [
            load_scaled_image("../resources/goblin/020.png"),
            load_scaled_image("../resources/goblin/021.png"),
            load_scaled_image("../resources/goblin/022.png")
        ]
        self.hurt_left_images = [
            load_scaled_image("../resources/goblin/024.png"),
            load_scaled_image("../resources/goblin/025.png"),
            load_scaled_image("../resources/goblin/026.png")
        ]
        self.hurt_right_images = [
            load_scaled_image("../resources/goblin/027.png"),
            load_scaled_image("../resources/goblin/028.png"),
            load_scaled_image("../resources/goblin/029.png")
        ]

        self.death_down_images = [
            load_scaled_image("../resources/goblin/036.png"),
            load_scaled_image("../resources/goblin/037.png"),
            load_scaled_image("../resources/goblin/048.png"),
            load_scaled_image("../resources/goblin/059.png"),
            load_scaled_image("../resources/goblin/065.png"),
            load_scaled_image("../resources/goblin/062.png"),
            load_scaled_image("../resources/goblin/063.png"),
            load_scaled_image("../resources/goblin/064.png")
        ]
        self.death_up_images = [
            load_scaled_image("../resources/goblin/066.png"),
            load_scaled_image("../resources/goblin/067.png"),
            load_scaled_image("../resources/goblin/038.png"),
            load_scaled_image("../resources/goblin/039.png"),
            load_scaled_image("../resources/goblin/043.png"),
            load_scaled_image("../resources/goblin/040.png"),
            load_scaled_image("../resources/goblin/041.png"),
            load_scaled_image("../resources/goblin/042.png")
        ]
        self.death_left_images = [
            load_scaled_image("../resources/goblin/044.png"),
            load_scaled_image("../resources/goblin/045.png"),
            load_scaled_image("../resources/goblin/046.png"),
            load_scaled_image("../resources/goblin/047.png"),
            load_scaled_image("../resources/goblin/052.png"),
            load_scaled_image("../resources/goblin/051.png"),
            load_scaled_image("../resources/goblin/050.png"),
            load_scaled_image("../resources/goblin/049.png")
        ]
        self.death_right_images = [
            load_scaled_image("../resources/goblin/053.png"),
            load_scaled_image("../resources/goblin/054.png"),
            load_scaled_image("../resources/goblin/055.png"),
            load_scaled_image("../resources/goblin/056.png"),
            load_scaled_image("../resources/goblin/061.png"),
            load_scaled_image("../resources/goblin/057.png"),
            load_scaled_image("../resources/goblin/058.png"),
            load_scaled_image("../resources/goblin/060.png")
        ]
        self.max_steps = 25
        self.steps_in_current_direction = 0

    def can_move_to(self, x, y):
        # Chuyển đổi vị trí của người chơi thành chỉ số ô lưới của bản đồ
        x += (32 * 8)
        y += (32 * 8)
        tile_x = int(x // self.tile_size)  # Ép kiểu thành int
        tile_y = int(y // self.tile_size)  # Ép kiểu thành int

        # Kích thước của điểm va chạm nhỏ hơn, nằm trung tâm người chơi
        collision_size = 32  # kích thước của vùng va chạm nhỏ hơn (20x20)
        half_collision_size = collision_size // 2

        # Các điểm kiểm tra va chạm nhỏ hơn nằm ở trung tâm người chơi
        collision_points = [
            (x - half_collision_size, y - 32 / 2 + 20),  # Top-left corner of collision box
            (x + half_collision_size - 1, y - 32 / 2 + 20),  # Top-right corner
            (x - half_collision_size, y + 32),  # Bottom-left corner
            (x + half_collision_size - 1, y + 32)  # Bottom-right corner
        ]

        # Kiểm tra từng điểm va chạm có nằm trong mã bị chặn không
        for px, py in collision_points:
            tile_x = int(px // self.tile_size)  # Ép kiểu thành int
            tile_y = int(py // self.tile_size)  # Ép kiểu thành int

            if self.map[tile_y][tile_x] in self.blocked_code:
                return False  # Nếu một trong các điểm va chạm bị chặn thì trả về False

        return True  # Tất cả các điểm đều không bị chặn

    def move_towards_player(self, player_x, player_y):
        # Tính khoảng cách giữa goblin và người chơi
        distance = math.sqrt((player_x + 32 - self.worldX - 64 * 4) ** 2 + (player_y + 48 - self.worldY - 64 * 4) ** 2)
        newx, newy = self.worldX, self.worldY
        # Nếu khoảng cách nhỏ hơn 100 (hoặc giá trị tùy chỉnh), goblin sẽ tấn công

        if distance < 100:
            self.attack(player_x, player_y)
        else:
            # Nếu không tấn công, di chuyển về phía người chơi
            if player_x < (self.worldX + 64 * 4):
                self.direction = "left"
                newx -= self.speed
            elif player_x > (self.worldX + 64 * 4):
                self.direction = "right"
                newx += self.speed

            if player_y < (self.worldY + 64 * 4):
                self.direction = "up"
                newy -= self.speed
            elif player_y > (self.worldY + 64 * 4):
                self.direction = "down"
                newy += self.speed
            self.worldX, self.worldY = newx, newy

    def draw(self, screen, camera_offset_x, camera_offset_y):
        # Lựa chọn hình ảnh dựa trên trạng thái và hướng
        if self.state == "death":
            images = getattr(self, f"death_{self.direction}_images", None)
        elif self.state == "attack":
            images = getattr(self, f"attack_{self.direction}_images", None)
        elif self.state == "hurt":
            images = getattr(self, f"hurt_{self.direction}_images", None)
        else:
            images = getattr(self, f"{self.direction}_images", None)

        # Kiểm tra xem các hình ảnh có được tải thành công hay không
        if images is None or len(images) == 0:
            print(f"Lỗi: Không tìm thấy hình ảnh cho trạng thái '{self.state}' và hướng '{self.direction}'")
            return

        # Tiến hành đến hình ảnh hiện tại cho hoạt ảnh
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.current_frame = (self.current_frame + 1) % len(images)  # Update frame in a circular way
            self.animation_counter = 0

        # Lấy hình ảnh hiện tại cho khung hình và kiểm tra chỉ số khung
        if len(images) > 0:  # Đảm bảo có hình ảnh để vẽ
            current_image = images[self.current_frame % len(images)]  # Sử dụng modulo để đảm bảo không vượt quá chỉ số
            x = self.worldX + camera_offset_x
            y = self.worldY + camera_offset_y
            screen.blit(current_image, (x, y))

            # Draw a white outline exactly around the 64x64 image

            # Define the health bar dimensions and position
            health_bar_width = 64 * 8  # Match goblin's width
            health_bar_height = 10  # Height of the health bar
            health_bar_x = x + 32  # Position it above the goblin
            health_bar_y = y + 32 - health_bar_height - 5  # Slightly above the goblin's head

            # Calculate the width of the health portion based on current_hp and max_hp
            health_ratio = self.current_hp / self.max_hp
            health_fill_width = int(health_bar_width * health_ratio)

            # Draw the health bar background (red)
            pygame.draw.rect(screen, (200, 200, 200), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

            # Draw the health portion (green)
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_fill_width, health_bar_height))
        else:
            print("Không có hình ảnh để vẽ.")

    def move(self):
        # Change direction if max steps reached
        if self.steps_in_current_direction >= self.max_steps:
            self.direction = random.choice(["up", "down", "left", "right"])
            self.steps_in_current_direction = 0  # Reset step counter

        # Move the goblin in the selected direction
        new_x, new_y = self.worldX, self.worldY
        if self.direction == "up":
            new_y -= 5
        elif self.direction == "down":
            new_y += 5
        elif self.direction == "left":
            new_x -= 5
        elif self.direction == "right":
            new_x += 5

        # Move if possible and increment the step counter

    def attack(self, player_x, player_y):
        self.state = "attack"

    def hurt(self, screen):
        self.state = "hurt"

    def update(self, screen, camera_offset_x, camera_offset_y, player_x, player_y):
        if self.state == "death":
            if self.death_time == 0:
                self.death_time = time.time()
            images = getattr(self, f"death_{self.direction}_images", None)

            if images and len(images) > 0:  # Đảm bảo có hình ảnh để vẽ
                # Cập nhật khung hình cho hoạt ảnh chết, sau đó giữ nguyên khung cuối cùng khi hoàn thành
                if self.current_frame < len(images) - 1:
                    # Chỉ tăng `current_frame` khi chưa đạt khung cuối
                    self.animation_counter += 1
                    if self.animation_counter >= 10:  # Điều chỉnh tốc độ hoạt ảnh
                        self.current_frame += 1
                        self.animation_counter = 0

                # Lấy hình ảnh hiện tại từ chuỗi `images`
                current_image = images[self.current_frame]
                x = self.worldX + camera_offset_x
                y = self.worldY + camera_offset_y
                screen.blit(current_image, (x, y))

            if time.time() - self.death_time >= 3:
                return False
        else:
            # Switch between idle and move state to simulate wandering
            if self.state == "idle" and random.random() < 0.05:
                self.move()
            elif self.state == "move" and random.random() < 0.1:
                self.state = "idle"
            self.move_towards_player(player_x, player_y)
            # Draw the goblin on the screen
            self.draw(screen, camera_offset_x, camera_offset_y)
        return True
