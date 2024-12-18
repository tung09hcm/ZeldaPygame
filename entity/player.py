from entity.entity import Entity
import pygame
import os
import json
import math


class Player(Entity):
    def __init__(self, game_map):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha (Entity)
        self.respawn = False
        self.last_use_time = 0  # Track last usage time
        self.use_delay = 100  # Delay in milliseconds
        self.current_map = "starter"
        self.item_index = 0
        self.overWorld = True
        self.Mart = False
        self.Cave = False
        self.inventory_map = {
            "POTION": 3,
            "PORTALSTONE": 5,
            "FULLRESTORE": 7,
            "HYPERPOTION": 2,
            "MAXPOTION": 1,
            "SUPERPOTION": 10
        }
        self.inventory_list = list(self.inventory_map.items())

        self.player_save_game = False
        self.use = True
        self.remove = False
        self.show_inventory = False
        self.level = 1
        self.max_hp = 50
        self.current_hp = 50
        self.max_xp = 50
        self.current_xp = 20
        self.money = 500

        self.blocked_code = []
        self.map = game_map
        self.worldX = 17 * 64
        self.worldY = 16 * 64
        # Các biến riêng cho Player
        self.speed = 12
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
        self.tile_size = 64
        # Initialize animation
        self.current_frame = 0
        self.animation_counter = 0  # To control animation speed
        self.click = False
        self.attack = False
        self.attack_up = pygame.transform.scale2x(pygame.image.load("../resources/player/sword_up.png").convert_alpha())
        self.attack_down = pygame.transform.scale2x(
            pygame.image.load("../resources/player/sword_down.png").convert_alpha())
        self.attack_right = pygame.transform.scale2x(
            pygame.image.load("../resources/player/sword_right.png").convert_alpha())
        self.attack_left = pygame.transform.scale2x(
            pygame.image.load("../resources/player/sword_left.png").convert_alpha())

        self.init_collison("../resources/map/collison")
        self.load_player_data("player_data.json")

    def save_player_data(self, filename):
        # Chuẩn bị dữ liệu để lưu
        data = {
            "inventory_map": self.inventory_map,
            "player_save_game": self.player_save_game,
            "use": self.use,
            "remove": self.remove,
            "show_inventory": self.show_inventory,
            "level": self.level,
            "max_hp": self.max_hp,
            "current_hp": self.current_hp,
            "max_xp": self.max_xp,
            "current_xp": self.current_xp,
            "money": self.money,
            "worldX": self.worldX,
            "worldY": self.worldY,
            "speed": self.speed,
            "health": self.health,
            "attack_power": self.attack_power,
            "defense": self.defense,
            "direction": self.direction,
            "overworld": self.overWorld,
            "cave": self.Cave,
            "mart": self.Mart,
            "current_map": self.current_map
        }

        # Ghi dữ liệu vào file JSON
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Dữ liệu đã được lưu vào", filename)

    def load_player_data(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

                # Gán các thuộc tính của người chơi từ dữ liệu đã tải
                self.inventory_map = data.get("inventory_map", self.inventory_map)
                self.player_save_game = data.get("player_save_game", self.player_save_game)
                self.use = data.get("use", self.use)
                self.remove = data.get("remove", self.remove)
                self.show_inventory = data.get("show_inventory", self.show_inventory)
                self.level = data.get("level", self.level)
                self.max_hp = data.get("max_hp", self.max_hp)
                self.current_hp = data.get("current_hp", self.current_hp)
                self.max_xp = data.get("max_xp", self.max_xp)
                self.current_xp = data.get("current_xp", self.current_xp)
                self.money = data.get("money", self.money)
                self.worldX = data.get("worldX", self.worldX)
                self.worldY = data.get("worldY", self.worldY)
                self.speed = data.get("speed", self.speed)
                self.health = data.get("health", self.health)
                self.attack_power = data.get("attack_power", self.attack_power)
                self.defense = data.get("defense", self.defense)
                self.direction = data.get("direction", self.direction)
                self.overWorld = data.get("overworld", self.overWorld)
                self.Cave = data.get("cave", self.Cave)
                self.Mart = data.get("mart", self.Mart)
                self.current_map = data.get("current_map")

            # Đồng bộ inventory_list với inventory_map mới
            self.inventory_list = list(self.inventory_map.items())
            print("Dữ liệu đã được tải từ", filename)

        except FileNotFoundError:
            print(f"Không tìm thấy file {filename}, sử dụng giá trị mặc định.")

    def set_map(self, map):
        self.map = map

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

    def draw_stats_menu(self, screen):
        # Prepare font for text rendering
        font = pygame.font.Font(None, 24)
        # Colors for the menu and text
        DARK_GRAY = (40, 40, 40)
        LIGHT_GRAY = (200, 200, 200)
        WHITE = (255, 255, 255)
        GREEN = (34, 177, 76)
        BLUE = (0, 162, 232)

        menu_width, menu_height = 300, 550
        screen_rect = screen.get_rect()
        menu_x = (screen_rect.width - menu_width) // 2 - 100 + 60 - 150
        menu_y = (screen_rect.height - menu_height) // 2 - 70 + 40 + 30

        # Draw the background rectangle
        pygame.draw.rect(screen, DARK_GRAY, (menu_x, menu_y, menu_width, menu_height), border_radius=15)
        # Draw the background rectangle for item
        if self.inventory_list:
            pygame.draw.rect(screen, DARK_GRAY, (menu_x + 320, menu_y, menu_width, menu_height / 3), border_radius=15)

        # Get the current item's name
        if self.inventory_list:
            item_name = self.inventory_list[self.item_index][0]

            # Create the filename by appending '.png' to the item name
            image_filename = f"{item_name}.png"

            # Construct the full path to the image
            image_path = os.path.join("../resources/item/", image_filename)

            # Load the image
            try:
                item_image = pygame.transform.scale2x(pygame.image.load(image_path).convert_alpha())
                screen.blit(item_image, (menu_x + 320 + 10, menu_y + 10))
            except pygame.error as e:
                print(f"Unable to load image: {image_path}. Error: {e}")
            # Định nghĩa giới hạn chiều rộng và vị trí cho văn bản
            info_x = menu_x + 320 + 25 + 70
            info_y = menu_y + 25
            max_info_width = menu_width - 100  # Giới hạn chiều rộng cho văn bản thông tin

            # Văn bản thông tin vật phẩm
            item_info_text_potion = "A spray-type wound medicine. It restores HP by 20 points."
            item_info_portal_stone = "A special stone that instantly returns you to the nearest healing station."
            item_info_full_restore = "A medicine that fully restores the HP and heals any status problems."
            item_info_hyperpotion = "A spray-type wound medicine. It restores the HP by 200 points."
            item_info_maxpotion = "A spray-type wound medicine. It fully restores the HP."
            item_info_superpotion = "A spray-type wound medicine. It restores the HP by 50 points."
            # Chia văn bản thành nhiều dòng dựa trên chiều rộng giới hạn
            item_info_text = ""
            if item_name == "POTION":
                item_info_text = item_info_text_potion
            elif item_name == "PORTALSTONE":
                item_info_text = item_info_portal_stone
            elif item_name == "FULLRESTORE":
                item_info_text = item_info_full_restore
            elif item_name == "HYPERPOTION":
                item_info_text = item_info_hyperpotion
            elif item_name == "MAXPOTION":
                item_info_text = item_info_maxpotion
            elif item_name == "SUPERPOTION":
                item_info_text = item_info_superpotion

            words = item_info_text.split()
            lines = []
            current_line = words[0]

            for word in words[1:]:
                # Thêm từ tiếp theo và kiểm tra chiều rộng của dòng
                test_line = current_line + " " + word
                test_surface = font.render(test_line, True, LIGHT_GRAY)

                if test_surface.get_width() <= max_info_width:
                    current_line = test_line
                else:
                    # Nếu dòng quá dài, lưu dòng hiện tại và bắt đầu dòng mới
                    lines.append(current_line)
                    current_line = word

            # Thêm dòng cuối cùng
            lines.append(current_line)

            # Hiển thị từng dòng của văn bản, với khoảng cách giữa các dòng
            line_height = font.get_height() + 5
            for i, line in enumerate(lines):
                line_surface = font.render(line, True, LIGHT_GRAY)
                screen.blit(line_surface, (info_x, info_y + i * line_height))

        # Define positions for each stat label and value
        stats = [
            ("Level", self.level),
            ("Attack", self.attack_power),
            ("Defense", self.defense),
            ("Special Attack", math.ceil(self.attack_power * 1.2)),  # Example placeholder calculation
            ("Special Defense", math.ceil(self.defense * 1.1)),  # Example placeholder calculation
            ("HP", f"{self.current_hp}/{self.max_hp}"),
            ("EXP", f"{self.current_xp}/{self.max_xp}"),
            ("Money", f"{self.money}$")
        ]

        # Render each stat label and value
        y_offset = menu_y + 20  # Start position for text within the menu
        for stat_name, stat_value in stats:
            # Render the stat name
            name_surface = font.render(f"{stat_name}: ", True, WHITE)
            screen.blit(name_surface, (menu_x + 20, y_offset))

            # Render the stat value
            value_surface = font.render(str(stat_value), True, LIGHT_GRAY)
            screen.blit(value_surface, (menu_x + 200, y_offset))

            y_offset += 30  # Move down for the next stat

        # Inventory section
        inventory_y = y_offset + 20
        inventory_title = font.render("Inventory:", True, WHITE)
        screen.blit(inventory_title, (menu_x + 20, inventory_y))

        # Example inventory items (replace with actual items if available)

        item_y = inventory_y + 30
        if self.inventory_list:
            for i, item in enumerate(self.inventory_list):
                if i == self.item_index and not self.player_save_game:
                    arrow_points = [
                        (menu_x + 35, item_y + 7),  # Tip of the arrow
                        (menu_x + 20, item_y),  # Top of the arrow
                        (menu_x + 20, item_y + 14)  # Bottom of the arrow
                    ]
                    pygame.draw.polygon(screen, GREEN, arrow_points)
                    item_surface = font.render(f"{item[0]}", True, GREEN)
                    number_item_surface = font.render(f"{item[1]}", True, GREEN)
                else:
                    item_surface = font.render(f"{item[0]}", True, LIGHT_GRAY)
                    number_item_surface = font.render(f"{item[1]}", True, LIGHT_GRAY)
                screen.blit(item_surface, (menu_x + 40, item_y))
                screen.blit(number_item_surface, (menu_x + 200, item_y))
                item_y += 25  # Space out items in the inventory

        # Draw save game button
        # Set the font and render the text
        new_font = pygame.font.Font(None, 48)

        if not self.player_save_game:
            item_surface = new_font.render("Save Game", True, LIGHT_GRAY)

            if not self.use:
                use_item_surface = new_font.render("Use", True, LIGHT_GRAY)
            else:
                use_item_surface = new_font.render("Use", True, GREEN)
            if not self.remove:
                remove_item_surface = new_font.render("Remove", True, LIGHT_GRAY)
            else:
                remove_item_surface = new_font.render("Remove", True, GREEN)

        else:
            item_surface = new_font.render("Save Game", True, GREEN)
            use_item_surface = new_font.render("Use", True, LIGHT_GRAY)
            remove_item_surface = new_font.render("Remove", True, LIGHT_GRAY)

        # Calculate the rectangle size and position

        # SAVE
        text_rect = item_surface.get_rect(topleft=(menu_x + 55, 530 + 25))
        border_rect = text_rect.inflate(10, 10)  # Add padding around the text for the border
        # USE
        use_text_rect = use_item_surface.get_rect(topleft=(750 - 70 + 15, 540 - 340))
        use_border_rect = use_text_rect.inflate(10, 10)  # Add padding around the text for the border
        # REMOVE
        remove_text_rect = remove_item_surface.get_rect(topleft=(750 - 70 + 15 + 90, 540 - 340))
        remove_border_rect = remove_text_rect.inflate(10, 10)  # Add padding around the text for the border

        # Draw the border and then the text
        if not self.player_save_game:
            pygame.draw.rect(screen, WHITE, border_rect, 2)  # Border width of 2 pixels
            if self.inventory_list:
                if not self.use:
                    pygame.draw.rect(screen, WHITE, use_border_rect, 2)  # Border width of 2 pixels
                elif self.use and not self.player_save_game:
                    pygame.draw.rect(screen, GREEN, use_border_rect, 2)  # Border width of 2 pixels

                if not self.remove:
                    pygame.draw.rect(screen, WHITE, remove_border_rect, 2)  # Border width of 2 pixels
                elif self.remove and not self.player_save_game:
                    pygame.draw.rect(screen, GREEN, remove_border_rect, 2)  # Border width of 2 pixels

        else:
            pygame.draw.rect(screen, GREEN, border_rect, 2)  # Border width of 2 pixels
            if self.inventory_list:
                pygame.draw.rect(screen, WHITE, use_border_rect, 2)
                pygame.draw.rect(screen, WHITE, remove_border_rect, 2)

        screen.blit(item_surface, text_rect.topleft)
        if self.inventory_list:
            screen.blit(use_item_surface, use_text_rect.topleft)
            screen.blit(remove_item_surface, remove_text_rect.topleft)

    def draw_bars(self, screen):
        WHITE = (255, 255, 255)
        LIGHT_GRAY = (100, 100, 100)
        DARK_GRAY = (50, 50, 50)
        GREEN = (34, 177, 76)
        BLUE = (0, 162, 232)
        BLACK = (0, 0, 0)

        # Background for the entire bar section
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, 410, 80), border_radius=15)

        # HP Bar
        pygame.draw.rect(screen, LIGHT_GRAY, (5, 5, 400, 24), border_radius=10)
        pygame.draw.rect(screen, WHITE, (5, 5, 400, 24), 2, border_radius=10)
        hp_width = int((self.current_hp / self.max_hp) * 396)
        pygame.draw.rect(screen, GREEN, (7, 7, hp_width, 20), border_radius=10)

        # XP Bar
        pygame.draw.rect(screen, LIGHT_GRAY, (5, 40, 300, 14), border_radius=7)
        pygame.draw.rect(screen, WHITE, (5, 40, 300, 14), 2, border_radius=7)
        xp_width = int((self.current_xp / self.max_xp) * 296)
        pygame.draw.rect(screen, BLUE, (7, 42, xp_width, 10), border_radius=7)

        # Display HP text with black outline below the XP bar
        font = pygame.font.Font(None, 30)
        hp_text = f"Level: {self.level}     HP: {self.current_hp}/{self.max_hp}"

        # Set new position below the XP bar
        text_x, text_y = 5, 60

        # Render black outline by drawing text multiple times slightly offset
        text_surface = font.render(hp_text, True, BLACK)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Offsets for outline
            screen.blit(text_surface, (text_x + dx, text_y + dy))

        # Render the main white text
        text_surface = font.render(hp_text, True, WHITE)
        screen.blit(text_surface, (text_x, text_y))

    def can_move_to(self, x, y):
        # Chuyển đổi vị trí của người chơi thành chỉ số ô lưới của bản đồ
        x += 32
        y += 48
        tile_x = int(x // self.tile_size)  # Ép kiểu thành int
        tile_y = int(y // self.tile_size)  # Ép kiểu thành int

        # Kích thước của điểm va chạm nhỏ hơn, nằm trung tâm người chơi
        collision_size = 32  # kích thước của vùng va chạm nhỏ hơn (20x20)
        half_collision_size = collision_size // 2

        # Các điểm kiểm tra va chạm nhỏ hơn nằm ở trung tâm người chơi
        collision_points = [
            (x - half_collision_size, y - 48 / 2 + 20),  # Top-left corner of collision box
            (x + half_collision_size - 1, y - 48 / 2 + 20),  # Top-right corner
            (x - half_collision_size, y + 48),  # Bottom-left corner
            (x + half_collision_size - 1, y + 48)  # Bottom-right corner
        ]

        # Kiểm tra từng điểm va chạm có nằm trong mã bị chặn không
        for px, py in collision_points:
            tile_x = int(px // self.tile_size)  # Ép kiểu thành int
            tile_y = int(py // self.tile_size)  # Ép kiểu thành int
            if self.map[tile_y][tile_x] == 902:

                if self.direction == "up":
                    if self.map[tile_y - 1][tile_x] not in self.blocked_code:
                        self.map[tile_y][tile_x] = 730
                        self.map[tile_y - 1][tile_x] = 902
                        return True
                elif self.direction == "down":
                    if self.map[tile_y + 1][tile_x] not in self.blocked_code:
                        self.map[tile_y][tile_x] = 730
                        self.map[tile_y + 1][tile_x] = 902
                        return True
                elif self.direction == "left":
                    if self.map[tile_y][tile_x - 1] not in self.blocked_code:
                        self.map[tile_y][tile_x] = 730
                        self.map[tile_y][tile_x - 1] = 902
                        return True
                elif self.direction == "right":
                    if self.map[tile_y][tile_x + 1] not in self.blocked_code:
                        self.map[tile_y][tile_x] = 730
                        self.map[tile_y][tile_x + 1] = 902
                        return True

                return False

            if self.map[tile_y][tile_x] in self.blocked_code:
                return False  # Nếu một trong các điểm va chạm bị chặn thì trả về False

        return True  # Tất cả các điểm đều không bị chặn

    def go_back_to_health_station(self):
        self.current_map = "starter"
        self.worldX = 17 * 64
        self.worldY = 16 * 64
        self.current_hp = self.max_hp

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_k]:
            self.show_inventory = False
        if not self.show_inventory:

            tile_x = (self.worldX // self.tile_size)
            tile_y = (self.worldY // self.tile_size)
            new_x, new_y = self.worldX, self.worldY

            if keys[pygame.K_SPACE]:
                if not self.show_inventory:
                    self.show_inventory = True

            if keys[pygame.K_w]:
                new_y -= self.speed
                self.direction = "up"
                self.click = True
            elif keys[pygame.K_s]:
                new_y += self.speed
                self.direction = "down"
                self.click = True
            elif keys[pygame.K_a]:
                new_x -= self.speed
                self.direction = "left"
                self.click = True
            elif keys[pygame.K_d]:
                new_x += self.speed
                self.direction = "right"
                self.click = True

            # Chỉ cập nhật vị trí nếu ô tiếp theo không bị chặn
            if self.can_move_to(new_x, new_y):
                self.worldX, self.worldY = new_x, new_y
        else:
            if keys[pygame.K_w] and current_time - self.last_use_time > self.use_delay:

                self.last_use_time = current_time
                if self.player_save_game:
                    self.item_index = len(self.inventory_list) - 1
                    self.player_save_game = False
                    return

                if self.item_index == 0:
                    return
                self.item_index -= 1
                self.player_save_game = False
            elif keys[pygame.K_s] and current_time - self.last_use_time > self.use_delay:
                self.last_use_time = current_time
                self.item_index += 1
                if len(self.inventory_list) <= self.item_index:
                    self.item_index = len(self.inventory_list) - 1
                    self.player_save_game = True
            elif keys[pygame.K_d] and current_time - self.last_use_time > self.use_delay:
                self.use = False
                self.remove = True
            elif keys[pygame.K_a] and current_time - self.last_use_time > self.use_delay:
                self.use = True
                self.remove = False
            # tương tác item
            elif keys[pygame.K_j] and current_time - self.last_use_time > self.use_delay:
                self.last_use_time = current_time
                if self.player_save_game:
                    print("save game")
                    self.save_player_data("player_data.json")
                elif self.use:

                    print("use " + self.inventory_list[self.item_index][0])

                    # Lấy tên khóa từ inventory_list dựa trên chỉ số item_index
                    item_name = self.inventory_list[self.item_index][0]

                    if item_name == "FULLRESTORE":
                        self.current_hp = self.max_hp
                    elif item_name == "HYPERPOTION":
                        self.current_hp += 200
                    elif item_name == "MAXPOTION":
                        self.current_hp = self.max_hp
                    elif item_name == "POTION":
                        self.current_hp += 20
                    elif item_name == "SUPERPOTION":
                        self.current_hp += 50
                    elif item_name == "PORTALSTONE":
                        self.go_back_to_health_station()
                        self.respawn = True
                    if self.current_hp > self.max_hp:
                        self.current_hp = self.max_hp

                    # Cập nhật số lượng item trong inventory_map
                    self.inventory_map[item_name] -= 1
                    if self.inventory_map[item_name] <= 0:
                        # Lấy tên khóa từ inventory_list dựa trên chỉ số item_index
                        item_name = ""
                        if len(self.inventory_list) > 0:
                            item_name = self.inventory_list[self.item_index][0]

                        # Xóa phần tử trong inventory_map theo tên khóa
                        if item_name in self.inventory_map:
                            del self.inventory_map[item_name]
                            self.item_index = 0

                    # Làm mới lại inventory_list để đồng bộ với inventory_map
                    self.inventory_list = list(self.inventory_map.items())

                elif self.remove:

                    # Lấy tên khóa từ inventory_list dựa trên chỉ số item_index
                    item_name = ""
                    if len(self.inventory_list) > 0:
                        item_name = self.inventory_list[self.item_index][0]

                    # Xóa phần tử trong inventory_map theo tên khóa
                    if item_name in self.inventory_map:
                        del self.inventory_map[item_name]
                        self.item_index = 0

                    # Làm mới lại inventory_list để đồng bộ với inventory_map
                    self.inventory_list = list(self.inventory_map.items())

                    print("remove " + item_name)

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

    def draw(self, screen, camera_offset_x, camera_offset_y):

        # print("worldX: " + str(self.worldX // 64) + " worldY: " + str(self.worldY // 64))

        # Calculate on-screen position
        screen_x = self.worldX + camera_offset_x
        screen_y = self.worldY + camera_offset_y
        # Draw stats menu if inventory is shown
        if self.show_inventory:
            self.draw_stats_menu(screen)

        # Select the correct animation based on direction
        if not self.click:
            if self.direction == "down":
                self.image = self.down_images[3]
            elif self.direction == "left":
                self.image = self.left_images[3]
            elif self.direction == "right":
                self.image = self.right_images[3]
            elif self.direction == "up":
                self.image = self.up_images[3]

        if self.direction == "up":
            self.image = self.up_images[self.current_frame]
        elif self.direction == "down":
            self.image = self.down_images[self.current_frame]
        elif self.direction == "left":
            self.image = self.left_images[self.current_frame]
        elif self.direction == "right":
            self.image = self.right_images[self.current_frame]

        # Draw player with calculated offset
        # if not self.show_inventory:
        screen.blit(self.image, (screen_x, screen_y))

        self.draw_bars(screen)

        RED = (255, 0, 0)
        pygame.draw.circle(screen, RED, (screen_x, screen_y), 3)

    def printCoordinate(self):
        tilex = self.worldX // self.tile_size
        tiley = self.worldY // self.tile_size
        print("====================")
        print("titlex" + str(tilex))
        print("titley" + str(tiley))
        print("====================")

    def checkgomart(self):
        tilex = self.worldX // self.tile_size
        tiley = self.worldY // self.tile_size

        if tilex == 11 and tiley == 14:
            self.overWorld = False
            self.Mart = True
            self.Cave = False
            print("Enter the MART")
        elif (tilex == 16 or tilex == 15) and tiley == 41:
            self.overWorld = False
            self.Mart = False
            self.Cave = True
            print("Enter the CAVE")

    def checkgobackOverworld(self):
        tilex = self.worldX // self.tile_size
        tiley = self.worldY // self.tile_size

        if tilex == 16 and tiley == 19:
            self.overWorld = True
            self.Mart = False
            self.Cave = False
            print("Enter the Overworld")
