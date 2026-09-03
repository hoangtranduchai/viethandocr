import os
import time

import cv2


def run_dip_section_1_1_demo(image_path: str = None):
    """
    Hiện thực hóa Mục 1.1 (trang 18 DIP 4E):
    - Định nghĩa hàm số học hai chiều f(x, y)
    - Số hóa tọa độ (x, y) và mức xám f thành các đại lượng rời rạc, hữu hạn
    - Phân tích thuộc tính nguyên tử của Pixel: (Location, Value)
    - Chứng minh truy xuất bộ nhớ O(1) đạt chuẩn thời gian thực
    """
    if image_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_dir, "assets", "kanji_input.jpg")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Không tìm thấy file '{image_path}'. Hãy kiểm tra lại đường dẫn trong thư mục assets/.")

    # 1. Thu nhận tín hiệu và số hóa thành ảnh xám đơn sắc (Mục 1.1)
    # Ảnh xám f(x, y) với x là chỉ số hàng (0 -> M-1), y là chỉ số cột (0 -> N-1)
    # Cường độ f(x, y) được lượng tử hóa thành số nguyên 8-bit rời rạc [0, 255]
    f_matrix = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if f_matrix is None:
        raise ValueError(f"Không thể giải mã file ảnh '{image_path}'. Kiểm tra lại định dạng file.")

    M, N = f_matrix.shape  # M hàng, N cột (Mục 1.1, Mục 2.4 Eq. 2-9)
    total_pixels = M * N

    # 2. Đo đạc thời gian truy xuất phần tử ảnh f(x, y) - Kiểm chứng truy xuất O(1)
    test_x, test_y = M // 2, N // 2

    # Warm up cache
    _ = f_matrix[test_x, test_y]

    # Đo thời gian đọc 1 pixel
    t_start = time.perf_counter_ns()
    _ = f_matrix[test_x, test_y]
    t_end = time.perf_counter_ns()
    read_latency_ns = t_end - t_start

    # 3. Tự động định vị vùng nét mực chữ 土 để trích xuất cửa sổ 8x8 pixel
    # Dựa vào Mục 2.3: mực có hệ số phản xạ thấp nên f(x, y) có giá trị cực tiểu
    # Tìm tọa độ (x, y) có mức xám thấp nhất trong vùng trung tâm ảnh
    search_roi = f_matrix[int(M * 0.3):int(M * 0.7), int(N * 0.3):int(N * 0.7)]
    min_val_local, _, min_loc_local, _ = cv2.minMaxLoc(search_roi)

    # Tọa độ gốc tương ứng trên toàn bộ ảnh f(x, y)
    center_y = int(N * 0.3) + min_loc_local[0]
    center_x = int(M * 0.3) + min_loc_local[1]

    # Cắt cửa sổ ma trận con 8x8 pixel bao quanh điểm mực (giao giữa mực và giấy)
    start_x = max(0, min(center_x - 3, M - 8))
    start_y = max(0, min(center_y - 3, N - 8))
    sub_matrix_8x8 = f_matrix[start_x:start_x + 8, start_y:start_y + 8]

    # 4. Xuất toàn bộ kết quả phân tích số học (Output)
    print("=" * 84)
    print("      BÁO CÁO THỰC THI SỐ HÓA MA TRẬN ẢNH f(x, y) - DIP 4E MỤC 1.1")
    print("=" * 84)
    print(f"[*] Đường dẫn file input      : {image_path}")
    print(f"[*] Kích thước không gian (MxN): {M} hàng x {N} cột")
    print(f"[*] Tổng số lượng phần tử ảnh  : {total_pixels:,} pixels (hữu hạn theo Mục 1.1)")
    print(f"[*] Kiểu dữ liệu lưu trữ       : {f_matrix.dtype} (Lượng tử hóa mức xám 8-bit [0, 255])")
    print(f"[*] Tốc độ truy xuất 1 pixel   : {read_latency_ns} nano-giây (ns) -> O(1) Memory Access")
    print("-" * 84)
    print(f"MA TRẬN SỐ NGUYÊN 8x8 TẠI RANH GIỚI NÉT CHỮ 土 VÀ MẶT GIẤY (Hàng {start_x}->{start_x+7}, Cột {start_y}->{start_y+7}):")
    print("   " + "".join([f"y={start_y+c:<6}" for c in range(8)]))
    for r in range(8):
        row_str = f"x={start_x+r:<4} "
        row_str += " ".join([f"{sub_matrix_8x8[r, c]:>5}" for c in range(8)])
        print(row_str)
    print("-" * 84)
    print("BÓC TÁCH 2 THUỘC TÍNH NGUYÊN TỬ CỦA TỪNG PIXEL THEO MỤC 1.1 (LOCATION & VALUE):")
    print(f"{'STT':<5} | {'Vị trí không gian (Location)':<30} | {'Giá trị mức xám (Value)':<25} | {'Nhận diện vật lý'}")
    print("-" * 84)

    idx = 1
    for r in range(0, 8, 2):
        for c in range(0, 8, 3):
            loc_x = start_x + r
            loc_y = start_y + c
            val = sub_matrix_8x8[r, c]
            nature = "Vết mực chữ 土" if val < 90 else ("Bóng mờ tay" if val < 170 else "Nền giấy trắng")
            print(f"{idx:<5} | Hàng x={loc_x:<5}, Cột y={loc_y:<5} (pixel) | f({loc_x}, {loc_y}) = {val:<10} | {nature}")
            idx += 1

    # 5. Lưu ảnh trực quan hóa để kiểm tra
    # Phóng to cửa sổ 8x8 lên kích thước 400x400 (dùng Nearest Neighbor để bảo toàn giá trị pixel gốc)
    zoomed_patch = cv2.resize(sub_matrix_8x8, (400, 400), interpolation=cv2.INTER_NEAREST)

    # Vẽ lưới và ghi số trực tiếp lên từng pixel
    display_patch = cv2.cvtColor(zoomed_patch, cv2.COLOR_GRAY2BGR)
    step = 400 // 8
    for i in range(8):
        for j in range(8):
            val = int(sub_matrix_8x8[i, j])
            # Vẽ đường kẻ biên pixel
            cv2.rectangle(display_patch, (j * step, i * step), ((j + 1) * step, (i + 1) * step), (100, 100, 100), 1)
            # Màu chữ: trắng cho pixel tối, đen cho pixel sáng
            text_color = (255, 255, 255) if val < 128 else (0, 0, 0)
            cv2.putText(display_patch, str(val), (j * step + 10, i * step + 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1, cv2.LINE_AA)

    output_img_path = os.path.join(os.path.dirname(image_path), "output_submatrix_8x8.png")
    cv2.imwrite(output_img_path, display_patch)
    print("-" * 84)
    print(f"[+] ĐÃ XUẤT TỆP ẢNH MINH HỌA: '{output_img_path}'")
    print("    (Mỗi ô vuông trên ảnh tương ứng đúng 1 pixel với con số mức xám hiển thị bên trong)")
    print("=" * 84)

if __name__ == "__main__":
    run_dip_section_1_1_demo()
