from entity.entity import Entity
import pygame
import os
import json
import random
import math
import time


class Goblin(Entity):
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
        self.worldX = random.randint(17, 29) * 64
        self.worldY = random.randint(5, 15) * 64
        self.level = random.randint(1, 3)
        self.max_hp = random.randint(25, 30)
        self.current_hp = self.max_hp
        self.exp = random.randint(10, 15)
        self.money = random.randint(10, 20)
        self.direction = "down"
        self.state = "idle"  # Possible states: idle, attack, hurt, move
        self.speed = 3
        self.attack_power = random.randint(3, 5)
        self.defense = random.randint(1, 2)
        self.map = game_map
        self.current_frame = 0
        self.animation_counter = 0

        self.death_time = 0

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

        self.death_down_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/036.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/037.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/048.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/059.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/065.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/062.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/063.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/064.png").convert_alpha())
        ]
        self.death_up_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/066.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/067.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/038.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/039.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/043.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/040.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/041.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/042.png").convert_alpha())
        ]
        self.death_left_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/044.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/045.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/046.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/047.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/052.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/051.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/050.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/049.png").convert_alpha())
        ]
        self.death_right_images = [
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/053.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/054.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/055.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/056.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/061.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/057.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/058.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("../resources/goblin/060.png").convert_alpha())
        ]
        self.max_steps = 25
        self.steps_in_current_direction = 0

    def can_move_to(self, x, y):
        # Chuyển đổi vị trí của người chơi thành chỉ số ô lưới của bản đồ
        x += 32
        y += 32
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

    def check_collision_with_other_goblins(self, goblins, min_distance=64):
        # Kiểm tra xem goblin hiện tại có quá gần các goblin khác không
        for other_goblin in goblins:
            if other_goblin != self:  # Không so sánh với chính nó
                distance = math.sqrt(
                    (other_goblin.worldX - self.worldX) ** 2 + (other_goblin.worldY - self.worldY) ** 2)
                if distance < 100:
                    # Nếu quá gần, điều chỉnh vị trí của goblin
                    if self.worldX < other_goblin.worldX:
                        self.worldX -= self.speed
                    else:
                        self.worldX += self.speed

                    if self.worldY < other_goblin.worldY:
                        self.worldY -= self.speed
                    else:
                        self.worldY += self.speed

    def move_towards_player(self, player_x, player_y):
        # Tính khoảng cách giữa goblin và người chơi
        distance = math.sqrt((player_x - self.worldX) ** 2 + (player_y - self.worldY) ** 2)
        newx, newy = self.worldX, self.worldY
        # Nếu khoảng cách nhỏ hơn 100 (hoặc giá trị tùy chỉnh), goblin sẽ tấn công
        if distance < 32:
            self.attack(player_x, player_y)
        else:
            # Nếu không tấn công, di chuyển về phía người chơi
            if player_x < self.worldX:
                self.direction = "left"
                newx -= self.speed
            elif player_x > self.worldX:
                self.direction = "right"
                newx += self.speed

            if player_y < self.worldY:
                self.direction = "up"
                newy -= self.speed
            elif player_y > self.worldY:
                self.direction = "down"
                newy += self.speed

            if self.can_move_to(newx, newy):
                self.worldX, self.worldY = newx, newy
                self.state = "move"  # Đặt trạng thái là di chuyển

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
            outline_color = (255, 255, 255)  # White color
            outline_rect = pygame.Rect(x, y, 128, 128)  # Outline rectangle exactly the same size as the image
            hitbox_rect = pygame.Rect(x + 32, y + 32, 64, 64)
            pygame.draw.rect(screen, outline_color, outline_rect, width=1)
            pygame.draw.rect(screen, outline_color, hitbox_rect, width=1)

            # Define the health bar dimensions and position
            health_bar_width = 64  # Match goblin's width
            health_bar_height = 6  # Height of the health bar
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

        if self.can_move_to(new_x, new_y):
            self.worldX = new_x
            self.worldY = new_y
            self.steps_in_current_direction += 1

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
