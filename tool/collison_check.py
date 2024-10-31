# Đường dẫn đến file TXT
file_path = "../resources/map/collison"

# Danh sách để lưu các mã bị chặn
blocked_codes = []

# Đọc file và kiểm tra giá trị
with open(file_path, 'r') as file:
    lines = file.readlines()

    for i in range(0, len(lines), 2):  # Bước qua từng cặp dòng
        code = lines[i].strip()  # Mã
        is_blocked = lines[i + 1].strip()  # Giá trị true/false

        if is_blocked.lower() == 'true':  # Kiểm tra nếu là true
            # Lấy số từ mã (giả sử mã có định dạng như '000.png')
            number = int(code.split('.')[0])  # Lấy phần trước dấu '.'
            blocked_codes.append(number)  # Thêm số vào danh sách

# In danh sách mã bị chặn
print(blocked_codes)
