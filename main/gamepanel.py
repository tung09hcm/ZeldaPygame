import pygame
from entity.player import Player


class GamePanel:
    def __init__(self, width=992, height=624, title="My Pygame Window"):
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
        for i in range(684):
            filename = f"../resources/pokemon_directory/{i:03}.png"
            image = pygame.image.load(filename).convert_alpha()
            scaled_image = (pygame.transform.scale2x(image))  # Scale the image 4x
            self.title.append(scaled_image)

        # Load map from file
        self.map = []
        self.intialize_map("../resources/map/starter")

        # Camera offset initialized to (0,0)
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.player = Player(self.map)


    def intialize_map(self, file_map):
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

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.calculate_camera_offset()

            self.window.fill(self.background_color)
            self.draw_map()

            # Draw player with camera offset
            self.player.handle_keys()
            self.player.update_animation()
            self.player.draw(self.window, self.camera_offset_x, self.camera_offset_y)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()