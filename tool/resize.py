from PIL import Image
import os

# Đường dẫn đến thư mục chứa ảnh
folder_path = "../resources/player"

# Duyệt qua tất cả các file trong thư mục
for filename in os.listdir(folder_path):
    # Kiểm tra nếu file là ảnh (đuôi .png)
    if filename.endswith(".png"):
        file_path = os.path.join(folder_path, filename)

        # Mở ảnh
        with Image.open(file_path) as img:
            # Thu nhỏ ảnh xuống 32x32
            resized_img = img.resize((32, 48), Image.LANCZOS)

            # Lưu ảnh lại (ghi đè lên file gốc)
            resized_img.save(file_path)

print("Thu nhỏ tất cả ảnh xuống 32x32 thành công!")
