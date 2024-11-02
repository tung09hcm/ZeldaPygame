from PIL import Image
import os


def combine_images_in_directory(folder_path, background_name, start_overlay, end_overlay, output_folder):
    """
    Kết hợp ảnh nền với các ảnh overlay trong một thư mục.

    :param folder_path: Đường dẫn tới thư mục chứa ảnh
    :param background_name: Tên file ảnh nền (layer dưới)
    :param start_overlay: Số thứ tự bắt đầu của ảnh overlay
    :param end_overlay: Số thứ tự kết thúc của ảnh overlay
    :param output_folder: Thư mục lưu các ảnh kết quả
    """
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Đường dẫn ảnh nền
    background_path = os.path.join(folder_path, f"{background_name}.png")
    # Mở ảnh nền
    background = Image.open(background_path).convert("RGBA")

    # Duyệt qua các ảnh overlay
    for overlay_index in range(start_overlay, end_overlay + 1):
        overlay_name = f"{str(overlay_index).zfill(3)}.png"
        overlay_path = os.path.join(folder_path, overlay_name)

        # Kiểm tra nếu ảnh overlay tồn tại
        if os.path.exists(overlay_path):
            overlay = Image.open(overlay_path).convert("RGBA")

            # Kết hợp ảnh overlay với ảnh nền
            combined = background.copy()  # Sao chép ảnh nền để giữ nguyên ảnh gốc
            combined.paste(overlay, (0, 0), overlay)  # Overlay tại góc trên cùng bên trái (0, 0)

            # Lưu ảnh kết quả
            output_path = os.path.join(output_folder, f"{overlay_name}")
            combined.save(output_path, "PNG")
            print(f"Đã lưu ảnh kết hợp: {output_path}")


# Ví dụ sử dụng
combine_images_in_directory(
    folder_path="../resources/pokemon_directory/combined",
    background_name="839",
    start_overlay=786,
    end_overlay=901,
    output_folder="../resources/pokemon_directory/combined/combined"
)
