from PIL import Image

def cut_image(image_path, output_folder):
    # Mở file hình ảnh
    img = Image.open(image_path)

    # Kích thước của ô
    tile_width = 32
    tile_height = 32

    # Kích thước của hình ảnh
    img_width, img_height = img.size

    # Đếm số lượng ô trên hàng và cột
    cols = img_width // tile_width
    rows = img_height // tile_height

    # Cắt ảnh và lưu các ô
    for row in range(rows):
        for col in range(cols):
            # Tính toán tọa độ ô
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height

            # Cắt ô
            tile = img.crop((left, upper, right, lower))

            # Đặt tên cho file
            tile_name = f"{row * cols + col + 1 + 50}.png"  # Tên từ 1 đến 12

            # Lưu ô vào thư mục output
            tile.save(f"{output_folder}/{tile_name}")

# Sử dụng hàm
cut_image("Dungeoncave.png", "../resources/map")
