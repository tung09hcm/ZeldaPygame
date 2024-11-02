import os

# Đường dẫn tới thư mục chứa ảnh
folder_path = "../resources/pokemon_directory/combined"

# Giá trị bắt đầu cho việc đặt tên (bắt đầu từ 0 cho tên đầu tiên là "000.png")
start_number = 786

# Lấy danh sách các file trong thư mục và sắp xếp chúng
files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

# Bước 1: Đổi tên tạm thời để tránh xung đột tên
for index, filename in enumerate(files):
    # Tạo tên tạm thời với prefix để không trùng với tên file gốc
    temp_name = f"temp_{index}.tmp"
    old_path = os.path.join(folder_path, filename)
    temp_path = os.path.join(folder_path, temp_name)
    os.rename(old_path, temp_path)

# Bước 2: Đổi tên từ tạm thời sang tên cuối cùng với định dạng 000.png, 001.png, ...
for index, temp_name in enumerate(sorted(os.listdir(folder_path))):
    # Đặt tên mới cho file với định dạng ba chữ số
    new_name = f"{str(index + start_number).zfill(3)}.png"
    temp_path = os.path.join(folder_path, temp_name)
    new_path = os.path.join(folder_path, new_name)

    # Đổi tên file
    os.rename(temp_path, new_path)
    print(f"Đã đổi tên {temp_name} thành {new_name}")

print("Hoàn tất việc đổi tên các file!")
