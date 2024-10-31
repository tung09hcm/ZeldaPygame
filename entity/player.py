from entity.entity import Entity
import pygame
import math

class Player(Entity):
    def __init__(self, game_map):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha (Entity)
        self.show_inventory = False
        self.level = 1
        self.max_hp = 50
        self.current_hp = 50
        self.max_xp = 50
        self.current_xp = 20

        self.blocked_code = []
        self.map = game_map
        self.worldX = 17*64
        self.worldY = 16*64
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
        self.attack_down = pygame.transform.scale2x(pygame.image.load("../resources/player/sword_down.png").convert_alpha())
        self.attack_right = pygame.transform.scale2x(pygame.image.load("../resources/player/sword_right.png").convert_alpha())
        self.attack_left = pygame.transform.scale2x(pygame.image.load("../resources/player/sword_left.png").convert_alpha())
        self.init_collison()
    def init_collison(self):
        with open("../resources/map/collison", 'r') as file:
            lines = file.readlines()

            for i in range(0, len(lines), 2):  # Bước qua từng cặp dòng
                code = lines[i].strip()  # Mã
                is_blocked = lines[i + 1].strip()  # Giá trị true/false

                if is_blocked.lower() == 'true':  # Kiểm tra nếu là true
                    # Lấy số từ mã (giả sử mã có định dạng như '000.png')
                    number = int(code.split('.')[0])  # Lấy phần trước dấu '.'
                    self.blocked_code.append(number)  # Thêm số vào danh sách

    def draw_stats_menu(self, screen):
        print("gọi hàm show stats menu")
        # Colors for the menu and text
        DARK_GRAY = (40, 40, 40)
        LIGHT_GRAY = (200, 200, 200)
        WHITE = (255, 255, 255)
        GREEN = (34, 177, 76)
        BLUE = (0, 162, 232)

        # Center the menu on the screen
        menu_width, menu_height = 300, 500
        screen_rect = screen.get_rect()
        menu_x = (screen_rect.width - menu_width) // 2 - 100 + 70 - 50
        menu_y = (screen_rect.height - menu_height) // 2 - 70 + 40

        # Draw the background rectangle
        pygame.draw.rect(screen, DARK_GRAY, (menu_x, menu_y, menu_width, menu_height), border_radius=15)

        # Prepare font for text rendering
        font = pygame.font.Font(None, 24)

        # Define positions for each stat label and value
        stats = [
            ("Level", self.level),
            ("Attack", self.attack_power),
            ("Defense", self.defense),
            ("Special Attack", self.attack_power * 1.2),  # Example placeholder calculation
            ("Special Defense", self.defense * 1.1),  # Example placeholder calculation
            ("HP", f"{self.current_hp}/{self.max_hp}"),
            ("EXP", f"{self.current_xp}/{self.max_xp}")
        ]

        # Render each stat label and value
        y_offset = menu_y + 20  # Start position for text within the menu
        for stat_name, stat_value in stats:
            # Render the stat name
            name_surface = font.render(f"{stat_name}: ", True, WHITE)
            screen.blit(name_surface, (menu_x + 20, y_offset))

            # Render the stat value
            value_surface = font.render(str(stat_value), True, LIGHT_GRAY)
            screen.blit(value_surface, (menu_x + 180, y_offset))

            y_offset += 30  # Move down for the next stat

        # Inventory section
        inventory_y = y_offset + 20
        inventory_title = font.render("Inventory:", True, WHITE)
        screen.blit(inventory_title, (menu_x + 20, inventory_y))

        # Example inventory items (replace with actual items if available)
        inventory_items = ["Potion x 5", "Shield", "Sword"]  # Placeholder items
        item_y = inventory_y + 30
        for item in inventory_items:
            item_surface = font.render(f"- {item}", True, LIGHT_GRAY)
            screen.blit(item_surface, (menu_x + 40, item_y))
            item_y += 25  # Space out items in the inventory

    # Usage: Inside the main game loop or event handler, call player.draw_stats_menu(screen)

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
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size

        # Các điểm kiểm tra va chạm xung quanh khung người chơi
        collision_points = [
            (x - self.tile_size // 2, y - 64 // 2),  # Top-left corner
            (x + self.tile_size // 2 - 1, y - 64 // 2),  # Top-right corner
            (x - self.tile_size // 2, y + 96 // 2 - 1),  # Bottom-left corner
            (x + self.tile_size // 2 - 1, y + 96 // 2 - 1)  # Bottom-right corner
        ]

        # Kiểm tra từng điểm va chạm có nằm trong mã bị chặn không
        for px, py in collision_points:
            tile_x = px // self.tile_size
            tile_y = py // self.tile_size
            # print(f"Điểm va chạm: ({tile_x}, {tile_y})")
            # if self.direction == "right":
            #     tile_x = tile_x + 1
            # elif self.direction == "down":
            #     tile_y = tile_y + 1
            if self.map[tile_y][tile_x] in self.blocked_code:
                return False  # Nếu một trong các điểm va chạm bị chặn thì trả về False

        return True  # Tất cả các điểm đều không bị chặn

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        tile_x = (self.worldX // self.tile_size)
        tile_y = (self.worldY // self.tile_size)
        new_x, new_y = self.worldX, self.worldY

        if keys[pygame.K_j]:
            self.attack = True
            self.speed = 7
        if keys[pygame.K_SPACE]:
            print("nhấn space")
            if not self.show_inventory:
                self.show_inventory = True
                print("true thành công")
        if keys[pygame.K_k]:
            print("nhấn escape")
            if self.show_inventory:
                self.show_inventory = False
                print("true thành công")
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

        # Calculate on-screen position
        screen_x = self.worldX + camera_offset_x - 48
        screen_y = self.worldY + camera_offset_y - 32
        if self.show_inventory == True:
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
        screen.blit(self.image, (screen_x, screen_y))

        if self.attack:
            if self.direction == "up":
                screen.blit(self.attack_up, (screen_x, screen_y-64))
            elif self.direction == "down":
                screen.blit(self.attack_down, (screen_x, screen_y+64))
            elif self.direction == "left":
                screen.blit(self.attack_left, (screen_x - 64, screen_y))
            elif self.direction == "right":
                screen.blit(self.attack_right, (screen_x + 64, screen_y))
            self.attack = False
            self.speed = 12
        if self.show_inventory == False:
            self.draw_bars(screen)