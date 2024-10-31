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

            # Đặt tên cho file với định dạng ba chữ số
            tile_index = row * cols + col  # Tính chỉ số bắt đầu từ 1
            tile_name = f"{tile_index:03}.png"  # Định dạng tên file với ba chữ số

            # Lưu ô vào thư mục output
            tile.save(f"{output_folder}/{tile_name}")


# Sử dụng hàm
cut_image("Dungeonforest.png", "../resources/dungeon")
