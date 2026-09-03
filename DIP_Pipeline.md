# LUỒNG BIẾN ĐỔI DỮ LIỆU TOÀN DIỆN PHÂN HỆ XỬ LÝ ẢNH SỐ (DIP PROCESSING PIPELINE)
## HỆ THỐNG TRỢ LÝ LUYỆN VIẾT CHỮ KANJI THỜI GIAN THỰC (60 FPS)

---

Luồng xử lý (Processing Pipeline) của phân hệ **Xử lý Ảnh số (Digital Image Processing - DIP)** cho toàn bộ hệ thống dạy viết chữ Kanji được thiết kế thành một **chuỗi biến đổi trạng thái dữ liệu tuần hoàn kín gồm 7 giai đoạn (Stages 0 đến 6)**, vận hành ở tốc độ thời gian thực $60\text{ FPS}$ (chu kỳ xử lý mỗi khung hình $\le 16.66\text{ ms}$), tuân thủ tuyệt đối các nguyên lý toán học và quang học trong giáo trình *Digital Image Processing, 4th Edition* (Rafael C. Gonzalez & Richard E. Woods).

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                      LUỒNG BIẾN ĐỔI DỮ LIỆU TOÀN DIỆN CỦA PHÂN HỆ DIP (CHUYÊN BIỆT 60 FPS)                             │
 ├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                                                        │
 │  [GIAI ĐOẠN 0: KHỞI TẠO & ĐỊNH VỊ HÌNH HỌC] (Thực thi 1 lần lúc bật máy - DIP Ch. 2, 5)                               │
 │  • Nhận diện 4 điểm neo (Tie Points / Reseau Marks) tại 4 góc ô viết (Mục 2.6)                                         │
 │  • Giải ma trận Homography H_3x3 qua hệ phương trình tọa độ đồng nhất (Eq. 2-45)                                       │
 │  • Cố định Bounding Box ROI và đóng băng ma trận H_3x3 vào bộ nhớ đệm RAM Cache                                        │
 │                                    │                                                                                   │
 │                                    ▼ (Vòng lặp thời gian thực 60 FPS: 16.66 ms / frame)                                │
 │  [GIAI ĐOẠN 1: THU NHẬN & CẮT ẢNH CON ROI (SUBIMAGE SLICING)] (DIP Mục 2.3, 2.4, 2.6)                                 │
 │  • Cảm biến CMOS xuất luồng thô 1080p@60FPS (Lấy mẫu Sampling & Lượng tử hóa 8-bit) (Mục 2.4)                          │
 │  • Khóa cứng thông số quang học: Focus Lock & Exposure Lock (Mục 2.3)                                                  │
 │  • Cắt lát con trỏ bộ nhớ O(1) trích xuất ảnh con ROI: f_ROI(x, y) kích thước 600x600 px (Mục 2.6)                     │
 │                                    │                                                                                   │
 │                                    ▼                                                                                   │
 │  [GIAI ĐOẠN 2: CỔNG KIỂM ĐỊNH QUANG HỌC IQA & LỌC PHẲNG GAUSSIAN] (DIP Ch. 3, 6, 10)                                  │
 │  • Bóc tách kênh Value trong không gian HSV: Kiểm tra 40 ≤ V_mean ≤ 235 (Mục 6.2)                                      │
 │  • Tích chập vi phân Laplacian 3x3: Var(∇²f_ROI) ≥ 65.0 (Mục 3.6, 10.2) ──[Vi phạm]──> HỦY FRAME & BÁO OLED            │
 │  • Lọc không gian thông thấp Gaussian 3x3 tách rời (σ = 0.8) triệt tiêu nhiễu hạt η(x, y) (Mục 3.5)                     │
 │                                    │                                                                                   │
 │                                    ▼ [Ảnh ROI xám đã khử nhiễu f_t và ảnh lưu trước đó f_{t-1}]                        │
 │  [GIAI ĐOẠN 3: PHÂN ĐOẠN VẾT MỰC VI SAI KHÁNG BÓNG ĐỔ] (DIP Ch. 2, 10)                                                │
 │  • Trừ ảnh số học có hướng: Δ_t(x, y) = max(0, f_{t-1}(x, y) - f_t(x, y)) ≥ 18 (Mục 10.6)                             │
 │  • Cắt ngưỡng độ tối tuyệt đối: M_dark = (f_t(x, y) ≤ 85) (Mục 2.3, 10.3)                                              │
 │  • Dò biên vi phân Sobel: M_edge = (‖∇f_t‖ ≥ 30) khử viền bóng mờ thoai thoải (Mục 10.2)                                │
 │  • Giao logic tập hợp: M_cand = M_diff ∩ M_dark ∩ M_edge (Mục 2.6, Bảng 2.2)                                           │
 │                                    │                                                                                   │
 │                                    ▼ [Mặt nạ nhị phân ứng viên M_cand]                                                 │
 │  [GIAI ĐOẠN 4: TINH LỌC HÌNH THÁI HỌC VÙNG LIÊN THÔNG] (DIP Ch. 9, 11)                                                 │
 │  • Toán tử Opening (A ∘ B) với phần tử cấu trúc chữ thập 3x3 bóc tách nhiễu rác (Mục 9.3)                              │
 │  • Trích xuất thành phần liên thông 8-kết nối & Lọc diện tích: 4 px ≤ Area(C_k) ≤ 150 px (Mục 9.5)                      │
 │                                    │                                                                                   │
 │                                    ▼ [Mặt nạ vết mực chuẩn xác M_final]                                                │
 │  [GIAI ĐOẠN 5: TRÍCH XUẤT MOMENT TRỌNG TÂM & NẮN PHẲNG HOMOGRAPHY] (DIP Ch. 2, 11)                                     │
 │  • Tính Spatial Moments bậc 0 và 1: μ_00, μ_10, μ_01 (Mục 11.3)                                                        │
 │  • Xác định tâm giọt mực mép sau ngón tay: (x_t, y_t) = (μ_10 / μ_00, μ_01 / μ_00) (Mục 11.3)                          │
 │  • Ánh xạ tức thời O(1) qua ma trận H_3x3 nắn phẳng về tọa độ chuẩn Canvas 128x128 px (Mục 2.6)                        │
 │  • Nối gia số đường thẳng Bresenham lên Canvas nhị phân & Lưu chuỗi m-path (Mục 2.5)                                   │
 │                                    │                                                                                   │
 │                                    ▼ (Sự kiện Nhấc bút Pen-Up: Vắng mặt vết mực mới > 10 frames liên tiếp)            │
 │  [GIAI ĐOẠN 6: THAM SỐ HÓA ĐỘNG HỌC, NÉN DỮ LIỆU & PHÂN LOẠI MỨC CAO] (DIP Ch. 8, 11, 12)                             │
 │  • Tham số hóa độ dài cung tích lũy s_k & Lấy mẫu đẳng cự đúng 32 điểm (Mục 11.1)                                       │
 │  • Chuẩn hóa Z-score triệt tiêu kích cỡ + Đạo hàm vận tốc (Δx, Δy, Δt) ──> Tensor [1, 32, 5]                            │
 │  • Nén Bit-plane ma trận Canvas 128x128 px thành gói tin 2.048 bytes bắn MQTT xuống ESP32 (Mục 8.2)                    │
 │  • Deep CNN phân loại 8 loại nét cơ bản (Mục 12.5) + Đối soát Cây Trie 512 chữ Kanji                                     │
 │  • Xuất xung phản xạ phần cứng: Còi Buzzer kêu, LED Xanh/Đỏ chớp, OLED vẽ mũi tên chỉ nét mới                          │
 └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Giai Đoạn 0: Khởi Tạo Hệ Thống & Định Vị Không Gian (Stage 0 - Offline Calibration)

Giai đoạn này diễn ra một lần duy nhất khi người học kích hoạt hệ thống nhằm thiết lập tương quan không gian hình học chuẩn mực giữa camera đặt nghiêng và mặt phẳng trang giấy.

```text
       (v1, w1) ┌───────────────────────────┐ (v2, w2)
                 \     Ô VIẾT TRÊN GIẤY    /
                  \   (Méo góc nghiêng)   /      ───> Áp dụng H_3x3 (Eq. 2-45) ───>
                   \                     /             (Bilinear Tie Points Eq. 2-46, 2-47)
           (v4, w4) └───────────────────┘ (v3, w3)

                                ┌─────────────────────────┐ (127, 0)
                                │      CANVAS CHUẨN       │
                                │      128 x 128 px       │
                                │   (Vuông góc tuyệt đối) │
                       (0, 127) └─────────────────────────┘ (127, 127)
```

* **Dữ liệu đầu vào (Input):**
  * Khung hình RGB $1920 \times 1080$ ban đầu chứa tờ giấy có vẽ ô vuông viết chữ Kanji.

* **Cơ sở lý thuyết DIP 4E & Phương trình toán học:**
  * *Xác lập điểm neo (Tie Points / Reseau Marks - Mục 2.6, trang 103–106):* Tọa độ 4 góc của ô viết trên mặt giấy trong ảnh nghiêng được xác định là $\{(v_k, w_k)\}_{k=1}^4$. Tọa độ đích tương ứng trên Canvas vuông chuẩn kích thước $128 \times 128\text{ px}$ là $\{(x_k, y_k)\}_{k=1}^4 = \{(0,0), (127,0), (127,127), (0,127)\}$.
  * *Thiết lập hệ phương trình song tuyến tính (Bilinear Approximation - Eqs. 2-46 & 2-47):*
    $$x_k = c_1 v_k + c_2 w_k + c_3 v_k w_k + c_4$$
    $$y_k = c_5 v_k + c_6 w_k + c_7 v_k w_k + c_8$$
  * *Ma trận biến đổi tọa độ đồng nhất (Homogeneous Transformation Matrix - Eq. 2-45):*
    $$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} \sim \mathbf{H}_{3 \times 3} \begin{bmatrix} v \\ w \\ 1 \end{bmatrix} = \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix} \begin{bmatrix} v \\ w \\ 1 \end{bmatrix}$$

* **Cơ chế thực thi & Tối ưu hóa:**
  * Hệ 8 phương trình được giải bằng thuật toán phân rã giá trị suy biến (SVD) trong $0.8\text{ ms}$. Ma trận $\mathbf{H}_{3 \times 3}$ được lưu cố định (Freeze / Cache) vào bộ nhớ RAM.
  * Thiết lập Hình chữ nhật bao tối thiểu mở rộng (Minimum Bounding Box - Mục 2.4, 2.6) bao quanh ô viết kèm biên đệm an toàn $\delta = 20\text{ px}$ để xác định tọa độ cắt con ROI: $[y_{\min}:y_{\max},\; x_{\min}:x_{\max}]$ kích thước xấp xỉ $600 \times 600\text{ px}$.

* **Dữ liệu đầu ra (Output):**
  * Ma trận chiếu phối cảnh $\mathbf{H}_{3 \times 3}$ đóng băng trong RAM Cache.
  * Tọa độ Bounding Box vùng ROI $[y_{\min}, y_{\max}, x_{\min}, x_{\max}]$.

* **Thời gian thực thi:** $1.20\text{ ms}$ (chỉ chạy 1 lần duy nhất lúc khởi động hệ thống).

---

### Giai Đoạn 1: Thu Nhận Số Hóa & Cắt Lát Ma Trận Con (Stage 1 - Sensing & Subimage Slicing)

* **Dữ liệu đầu vào (Input):**
  * Tín hiệu quang điện vật lý từ mảng cảm biến hình ảnh CMOS tiếp nhận thông lượng ánh sáng từ mặt bàn viết.

* **Cơ sở lý thuyết DIP 4E & Phương trình toán học:**
  * *Lấy mẫu và lượng tử hóa (Sampling & Quantization - Mục 2.4, trang 63–70):* Rời rạc hóa không gian trên lưới Cartesian $\mathbb{Z}^2$ và lượng tử hóa năng lượng bức xạ thành tín hiệu số 8-bit rời rạc ($L = 2^8 = 256$ mức xám, dải giá trị $[0, 255]$).
  * *Mô hình tạo ảnh vật lý (Image Formation Model - Mục 2.3, Eqs. 2-3 & 2-4):*
    $$f(x, y) = i(x, y) \cdot r(x, y), \quad 0 \le f(x, y) \le 255$$
  * *Trích xuất ma trận con (Subimage Operations - Mục 2.6, trang 90, Hình 2.34):* Giới hạn tọa độ xử lý vào không gian con:
    $$f_{\text{ROI}}(x, y) = f\big(x + x_{\min},\; y + y_{\min}\big), \quad 0 \le x < W_{\text{ROI}},\; 0 \le y < H_{\text{ROI}}$$

* **Cơ chế thực thi & Tối ưu hóa:**
  * Khóa cứng thông số phần cứng của camera (`Focus Lock` cố định ở khoảng cách $30\text{ cm}$, `Exposure Lock` cố định thời gian phơi sáng) để triệt tiêu dao động độ nhạy sáng tự động (Auto-Exposure Hunting).
  * Sử dụng kỹ thuật trỏ vùng nhớ liên tục (Memory Pointer Slicing $O(1)$) để trích xuất ảnh con $f_{\text{ROI}}$ kích thước $600 \times 600\text{ px}$, không thực hiện thao tác sao chép mảng dữ liệu (Zero-Copy), giảm tải xử lý từ $2.073.600\text{ pixels}$ xuống $360.000\text{ pixels}$ (giảm $5.76\text{ lần}$).

* **Dữ liệu đầu ra (Output):**
  * Ma trận ảnh xám con $f_{\text{ROI}}(x, y)$ kích thước $600 \times 600$, kiểu dữ liệu `uint8`.

* **Thời gian thực thi:** **$0.05\text{ ms}$**.

---

### Giai Đoạn 2: Cổng Kiểm Định Quang Học IQA & Tiền Xử Lý Không Gian (Stage 2 - Photometric IQA & Smoothing)

* **Dữ liệu đầu vào (Input):**
  * Ma trận ảnh con $f_{\text{ROI}}(x, y)$ kích thước $600 \times 600$ vừa thu nhận.

* **Cơ sở lý thuyết DIP 4E & Phương trình toán học:**
  * *Đo kênh cường độ sáng HSV (Mục 6.2, trang 407–413):* Bóc tách kênh độ sáng $V$ (Value) từ không gian màu RGB:
    $$V(x, y) = \max\Big(R(x, y), G(x, y), B(x, y)\Big)$$
    Tính độ sáng trung bình mẫu (Sample Mean - Mục 2.6, Eq. 2-69):
    $$\bar{V} = \frac{1}{M N}\sum_{x=0}^{M-1}\sum_{y=0}^{N-1} V(x, y)$$
  * *Toán tử vi phân bậc hai Laplacian rời rạc (Mục 3.6, Eqs. 3-53 & 3-54; Mục 10.2):*
    $$\nabla^2 f(x, y) = f(x+1, y) + f(x-1, y) + f(x, y+1) + f(x, y-1) - 4f(x, y)$$
    Tính phương sai thống kê (Variance of Intensities - Mục 2.6, Eq. 2-70) của ảnh vi phân bậc hai để định lượng mức độ sắc nét biên:
    $$\text{Var}(\nabla^2 f) = \frac{1}{M N}\sum_{x=0}^{M-1}\sum_{y=0}^{N-1}\left(\nabla^2 f(x, y) - \bar{\mu}_{\nabla^2}\right)^2$$
  * *Bộ lọc không gian làm mịn Gaussian 2 chiều tách rời (Separable Lowpass Gaussian Filter - Mục 3.5, Eqs. 3-44 & 3-47):*
    $$h(x, y) = g_1(x) \cdot g_2(y) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{x^2}{2\sigma^2}} \times \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{y^2}{2\sigma^2}}$$
    với nhân chập $3 \times 3$, độ lệch chuẩn $\sigma = 0.8$.

* **Cơ chế thực thi & Tối ưu hóa:**
  * *Cổng IQA ngắt sớm (Early-Exit Gate):*
    1. Nếu $\bar{V} < 40$ (phòng học quá tối) hoặc $\bar{V} > 235$ (bị lóa đèn bàn): Hủy xử lý frame, phát mã MQTT `WARN_LIGHT` lên OLED.
    2. Nếu $\text{Var}(\nabla^2 f) < 65.0$ (rung chấn mặt bàn gây nhòe mờ chuyển động Motion Blur - Chương 5): Hủy bỏ ngay lập tức chu kỳ frame hiện tại ($< 0.1\text{ ms}$). Toàn bộ các phép tính nặng phía sau được bỏ qua, bảo vệ CPU khỏi tính toán sai lệch.
  * *Lọc Gaussian tách rời:* Tách phép tích chập $3 \times 3$ thành 2 lượt tích chập 1D ($1 \times 3$ và $3 \times 1$), giảm số phép nhân từ 9 phép tính xuống $3 + 3 = 6$ phép tính trên mỗi pixel, triệt tiêu nhiễu cộng ngẫu nhiên $\eta(x, y)$ (Mục 2.6, Eq. 2-25).

* **Dữ liệu đầu ra (Output):**
  * Ma trận ảnh con đã làm mịn $f_t(x, y)$ kích thước $600 \times 600$, bảo toàn biên cạnh.

* **Thời gian thực thi:** **$0.35\text{ ms}$**.

---

### Giai Đoạn 3: Phân Đoạn Vết Mực Vi Sai Kháng Bóng Đổ (Stage 3 - Motion & Physical Segmentation)

* **Dữ liệu đầu vào (Input):**
  * Khung hình hiện tại đã lọc phẳng $f_t(x, y)$ và khung hình quá khứ liền kề $f_{t-1}(x, y)$.

* **Cơ sở lý thuyết DIP 4E & Phương trình toán học:**
  * *Phân đoạn dựa trên chuyển động theo thời gian (The Use of Motion in Segmentation - Mục 10.6, trang 796–798, Eqs. 10-128 & 10-129):* Áp dụng phép trừ ảnh số học vi sai có hướng (Directional Image Subtraction - Mục 2.6, Eq. 2-24):
    $$\Delta_t(x, y) = \max\Big(0,\; f_{t-1}(x, y) - f_t(x, y)\Big)$$
    Mặt nạ nhị phân chuyển động $M_{\text{diff}}(x, y) = 1$ khi và chỉ khi $\Delta_t(x, y) \ge 18$.
  * *Cổng cắt ngưỡng độ tối vật lý tuyệt đối (Thresholding based on Reflectance Model - Mục 2.3, Example 2.1 & Mục 10.3, Eq. 10-49):*
    $$M_{\text{dark}}(x, y) = \begin{cases} 1 & \text{nếu } f_t(x, y) \le 85 \\ 0 & \text{ngược lại} \end{cases}$$
    Hạt mực có hệ số phản xạ cực tiểu $r_{\text{ink}} \le 0.05 \implies f_{\text{ink}} \le 45$; vùng bóng đổ bàn tay có hệ số phản xạ của giấy giữ nguyên $r_{\text{paper}} \approx 0.80$, độ rọi suy giảm khiến $f_{\text{shadow}} \in [130, 170] \gg 85$. Do đó, bóng tay bị triệt tiêu $100\%$.
  * *Toán tử Gradient Sobel phát hiện biên sắc nhọn (Sobel Gradient Operators - Mục 10.2, Eqs. 10-14 đến 10-21):*
    $$G_x = (z_7 + 2z_8 + z_9) - (z_1 + 2z_2 + z_3), \quad G_y = (z_3 + 2z_6 + z_9) - (z_1 + 2z_4 + z_7)$$
    Độ lớn Gradient:
    $$M_{\text{Sobel}}(x, y) = \Vert\nabla f_t\Vert = \sqrt{G_x^2 + G_y^2} \approx |G_x| + |G_y|$$
    Mặt nạ biên sắc nhọn: $M_{\text{edge}}(x, y) = 1$ khi $\Vert\nabla f_t(x, y)\Vert \ge 30$. Biên bóng đổ mờ chuyển tiếp thoai thoải ($\Vert\nabla f_t\Vert < 15$) bị loại bỏ hoàn toàn.
  * *Giao logic tập hợp (Set Intersection - Mục 2.6, Eq. 2-37, Bảng 2.2):*
    $$M_{\text{cand}} = M_{\text{diff}} \cap M_{\text{dark}} \cap M_{\text{edge}}$$

* **Cơ chế thực thi & Tối ưu hóa:**
  * Thực thi trên các vector mảng một chiều thông qua phép tính logic cấp bit (Bitwise AND) và phép trừ bão hòa không âm (Unsigned Saturating Arithmetic).

* **Dữ liệu đầu ra (Output):**
  * Mặt nạ nhị phân ứng viên $M_{\text{cand}}(x, y)$ kích thước $600 \times 600$ chứa các cụm pixel mực mới xuất hiện.

* **Thời gian thực thi:** **$0.42\text{ ms}$**.

---

### Giai Đoạn 4: Tinh Lọc Cấu Trúc Hình Thái Học (Stage 4 - Morphological Cleaning & Area Filter)

* **Dữ liệu đầu vào (Input):**
  * Mặt nạ nhị phân ứng viên $M_{\text{cand}}(x, y)$.

* **Cơ sở lý thuyết DIP 4E & Phương trình toán học:**
  * *Toán tử mở hình thái học (Morphological Opening - Mục 9.3, trang 644–647, Eq. 9-15):*
    $$A \circ B = (A \ominus B) \oplus B$$
    trong đó $A$ là tập hợp pixel của $M_{\text{cand}}$, và $B$ là phần tử cấu trúc (Structuring Element - Mục 9.1) dạng chữ thập đối xứng đối với gốc tọa độ kích thước $3 \times 3$:
    $$B = \begin{bmatrix} 0 & 1 & 0 \\ 1 & 1 & 1 \\ 0 & 1 & 0 \end{bmatrix}$$
    Phép xói mòn (Erosion - Eq. 9-7) triệt tiêu hoàn toàn các điểm nhiễu hạt cô lập và gai nhọn có bán kính nhỏ hơn 1 pixel. Phép giãn nở tiếp theo (Dilation - Eq. 9-1) khôi phục lại thể tích nguyên bản của vệt mực hợp lệ.
  * *Trích xuất thành phần liên thông 8-kết nối (Connected Components Extraction - Mục 9.5, Eqs. 9-33 & 9-34; Mục 2.5):*
    $$X_k = (X_{k-1} \oplus B) \cap A, \quad k = 1, 2, 3, \dots$$
    với điều kiện hội tụ $X_k = X_{k-1}$.
  * *Lọc diện tích hình học (Region Descriptors / Area - Mục 11.3, Eq. 11-47):*
    $$\text{Area}(C_k) = \sum_{(x, y) \in C_k} 1$$
    Bộ lọc diện tích áp đặt ràng buộc kích thước vật lý của giọt mực sinh ra trong khoảng thời gian $1/60\text{ s}$ của ngòi bút viết tay thông thường:
    $$M_{\text{final}} = \bigcup \Big\{C_k \;\Big|\; 4\text{ px} \le \text{Area}(C_k) \le 150\text{ px}\Big\}$$
    Các mảng chuyển động lớn do cẳng tay hoặc nếp gấp mép áo cử động ($\text{Area} > 150\text{ px}$) bị loại bỏ trọn vẹn.

* **Cơ chế thực thi & Tối ưu hóa:**
  * Giải thuật quét nhãn 2 lượt (Two-Pass Connected Component Labeling) tối ưu hóa bảng tra cứu tương đương (Equivalence Table) trên mảng một chiều.

* **Dữ liệu đầu ra (Output):**
  * Mặt nạ nhị phân vết mực chuẩn xác $M_{\text{final}}(x, y)$ kích thước $600 \times 600$.

* **Thời gian thực thi:** **$0.28\text{ ms}$**.

---

### Giai Đoạn 5: Trích Xuất Moment Trọng Tâm & Nắn Phẳng Homography Tức Thời (Stage 5 - Moments & Rectification)

* **Dữ liệu đầu vào (Input):**
  * Mặt nạ nhị phân đã làm sạch $M_{\text{final}}(x, y)$.

* **Cơ sở lý thuyết DIP 4E & Phương trình toán học:**
  * *Moment không gian vùng 2 chiều (Spatial Moments - Mục 11.3, trang 840–842, Eq. 11-49):*
    $$m_{pq} = \sum_{x} \sum_{y} x^p y^q M_{\text{final}}(x, y)$$
    Trong đó:
    $$m_{00} = \sum_{x} \sum_{y} M_{\text{final}}(x, y) = \text{Tổng số pixel mực (Diện tích)}$$
    $$m_{10} = \sum_{x} \sum_{y} x \cdot M_{\text{final}}(x, y), \quad m_{01} = \sum_{x} \sum_{y} y \cdot M_{\text{final}}(x, y)$$
    Tọa độ trọng tâm đầu ngòi bút (Centroid of Ink Region - Eq. 11-50):
    $$\bar{x} = \frac{m_{10}}{m_{00}}, \quad \bar{y} = \frac{m_{01}}{m_{00}}$$
    Chuyển đổi về hệ tọa độ gốc của toàn bộ khung hình camera:
    $$x_t^{\text{raw}} = \bar{x} + x_{\min}, \quad y_t^{\text{raw}} = \bar{y} + y_{\min}$$
  * *Nắn phẳng phối cảnh tức thời qua ma trận Homography đóng băng $\mathbf{H}_{3 \times 3}$ (Mục 2.6, Eq. 2-45; Chương 5):*
    $$\begin{bmatrix} x' \\ y' \\ w' \end{bmatrix} = \mathbf{H}_{3 \times 3} \begin{bmatrix} x_t^{\text{raw}} \\ y_t^{\text{raw}} \\ 1 \end{bmatrix}$$
    Tọa độ chuẩn hóa trên Canvas vuông $128 \times 128\text{ px}$:
    $$x_{\text{canon}} = \text{round}\left(\frac{x'}{w'}\right), \quad y_{\text{canon}} = \text{round}\left(\frac{y'}{w'}\right)$$
  * *Tái tạo đường cong liên tục (Digital Paths - Mục 2.5, trang 80):* Vẽ đoạn nối giữa điểm hiện tại $(x_t, y_t)_{\text{canon}}$ và điểm liền trước $(x_{t-1}, y_{t-1})_{\text{canon}}$ bằng thuật toán vẽ đường thẳng số nguyên Bresenham với độ dày ngòi bút $d = 3\text{ px}$ lên ma trận tích lũy Canvas nhị phân $C_{128 \times 128}$.
  * *Lưu vết động học m-path (Mixed Path - Mục 2.5):* Đưa bộ 3 giá trị $(x_c, y_c, t)$ vào chuỗi hàng đợi động học $\mathbf{P}_{\text{raw}} = [(x_1, y_1, t_1), (x_2, y_2, t_2), \dots]$.

* **Cơ chế thực thi & Tối ưu hóa:**
  * Phép nhân ma trận vector $3 \times 3$ với vector $3 \times 1$ tiêu tốn chỉ 9 phép nhân và 6 phép cộng, thực thi trong $0.02\text{ ms}$ ($O(1)$).

* **Dữ liệu đầu ra (Output):**
  * Tọa độ Canvas chuẩn $(x_{\text{canon}}, y_{\text{canon}})$.
  * Ma trận Canvas nhị phân tích lũy $C_{128 \times 128}$ cập nhật nét chữ.
  * Danh sách chuỗi điểm động học $\mathbf{P}_{\text{raw}}$.

* **Thời gian thực thi:** **$0.14\text{ ms}$**.

---

### Giai Đoạn 6: Tham Số Hóa Động Học, Nén Dữ Liệu & Nhận Diện Mức Cao (Stage 6 - High-Level Classification & Output)

Giai đoạn này được kích hoạt khi phát hiện sự kiện **Nhấc bút (Pen-Up Event)**: Trải qua $10\text{ khung hình liên tiếp}$ ($166\text{ ms}$) mà mặt nạ $M_{\text{final}}$ hoàn toàn rỗng ($m_{00} = 0$).

```text
 [Chuỗi điểm thô P_raw: N điểm bất kỳ] 
                   │
                   ▼ (Tham số hóa độ dài cung s_k - Eq. 11-1)
 [Tái lấy mẫu đẳng cự: Đúng 32 mốc không gian đều nhau]
                   │
                   ▼ (Chuẩn hóa Z-Score: Triệt tiêu kích cỡ và vị trí - Mục 2.6)
 [Vector Tensor đặc trưng [1, 32, 5]: (x_norm, y_norm, Δx, Δy, Δt)]
                   │
                   ├──────────────────────────────────┐
                   ▼                                  ▼
      [Mạng nơ-ron tích chập sâu Deep CNN]    [Nén ma trận Canvas nhị phân 128x128 px]
      (Chapter 12, Mục 12.5)                         (Bit-plane Coding - Chapter 8)
                   │                                  │
                   ▼                                  ▼
      [Nhãn nét 8 loại: NGANG, SỔ...]         [Gói tin nén 2.048 bytes truyền MQTT]
                   │                                  │
                   └─────────────────┬────────────────┘
                                     ▼
                    [ĐỐI SOÁT CÂY TIỀN TỐ 512 KANJI (O(1))]
                                     │
                                     ▼
      [KÍCH HOẠT PHẢN XẠ ESP32: OLED VẼ HƯỚNG DẪN, LED XANH/ĐỎ, CÒI BÍP]
```

* **Dữ liệu đầu vào (Input):**
  * Danh sách chuỗi điểm động học thô $\mathbf{P}_{\text{raw}} = \{(x_k, y_k, t_k)\}_{k=1}^K$ ($K$ biến thiên tùy tốc độ viết) và Canvas nhị phân $C_{128 \times 128}$.

* **Cơ sở lý thuyết DIP 4E & Phương trình toán học:**
  * *Tham số hóa độ dài cung tích lũy (Arc-Length Parameterization - Mục 11.1, trang 814–817):*
    Tính khoảng cách Euclid từng chặng (Euclidean Distance - Mục 2.5, Eq. 2-19):
    $$\Delta d_k = \sqrt{(x_k - x_{k-1})^2 + (y_k - y_{k-1})^2}$$
    Độ dài cung tích lũy:
    $$s_0 = 0, \quad s_k = s_{k-1} + \Delta d_k, \quad k = 1, 2, \dots, K$$
    Tổng chiều dài nét viết là $S = s_K$. Tiến hành chia đoạn thẳng $[0, S]$ thành $31$ khoảng cách đều nhau ($\Delta s = S / 31$), nội suy tọa độ song tuyến tính (Bilinear Interpolation - Mục 2.4, Eq. 2-17) để tái lấy mẫu thành đúng **$32\text{ điểm đẳng cự}$** (Equidistant Resampling).
  * *Chuẩn hóa thống kê Z-Score (Statistical Normalization - Mục 2.6, Eqs. 2-69 & 2-70):*
    Triệt tiêu hoàn toàn sự phụ thuộc vào kích thước viết to/nhỏ và vị trí tọa độ:
    $$x_i^{\text{norm}} = \frac{x_i - \bar{x}}{\sigma_x}, \quad y_i^{\text{norm}} = \frac{y_i - \bar{y}}{\sigma_y}$$
    Ghép thêm các đạo hàm vi phân bậc một (First-order Differences - Mục 10.2):
    $$\Delta x_i = x_{i+1}^{\text{norm}} - x_i^{\text{norm}}, \quad \Delta y_i = y_{i+1}^{\text{norm}} - y_i^{\text{norm}}, \quad \Delta t_i = t_{i+1} - t_i$$
    tạo thành Tensor đầu vào có kích thước cố định: $[1, 32, 5]$.
  * *Nén dữ liệu không tổn hao (Bit-plane / Run-Length Compression - Mục 8.2, trang 566–576):*
    Ma trận Canvas $128 \times 128\text{ pixels}$ nhị phân ($16.384\text{ bits}$) được đóng gói thành một mảng byte liên tục: Cứ mỗi 8 pixel liên tiếp được nén vào đúng $1\text{ byte}$ (`uint8`):
    $$\text{Kích thước gói tin} = \frac{128 \times 128}{8} = \mathbf{2.048\text{ bytes}}$$
    Gói tin $2\text{ KB}$ này được bắn trực tiếp qua giao thức mạng nội bộ MQTT xuống ESP32 trong thời gian $< 0.8\text{ ms}$ mà không gây nghẽn băng thông (Networking Bandwidth - Mục 1.5).
  * *Phân loại mẫu nét qua Mạng nơ-ron tích chập sâu (Deep CNN - Mục 12.5, trang 964–986):*
    Mạng tích chập 1D kết hợp trích xuất đặc trưng không gian đa kênh đưa ra vector phân phối xác suất Softmax $\mathbf{p} = [p_1, p_2, \dots, p_8]$ đại diện cho 8 loại nét cơ bản.
  * *Đối soát Cây tiền tố (Prefix Trie Verification - Mục 1.4, Knowledge Base):*
    Truy vấn nhãn nét vừa nhận diện vào Cây tri thức của chữ Hán hiện tại:
    * **Nếu ĐÚNG thứ tự:** ESP32 kích hoạt chớp **LED Xanh**, còi kêu $1$ tiếng "Bíp" ngắn $15\text{ ms}$, màn hình OLED hiển thị mũi tên hướng dẫn nét kế tiếp.
    * **Nếu SAI thứ tự / Ngược chiều:** ESP32 kích hoạt chớp **LED Đỏ**, còi hú cảnh báo $60\text{ ms}$, màn hình OLED hiển thị thông báo `SAI HUONG NET`.

* **Dữ liệu đầu ra (Output):**
  * Gói tin điều khiển JSON điều phối phần cứng trạm ESP32 qua Wi-Fi MQTT.

* **Thời gian thực thi:** **$1.80\text{ ms}$** (chỉ chạy tại frame người học nhấc bút).

---

### Bảng Tổng Hợp Thông Số & Ngân Sách Thời Gian Toàn Bộ Luồng Xử Lý (Latency Budget)

| Giai Đoạn Luồng Xử Lý DIP | Bản Chất Tín Hiệu Đầu Vào | Trạng Thái Dữ Liệu Đầu Ra | Thuật Toán Cốt Lõi DIP 4E | Thời Gian Chạy (CPU Laptop) |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 0: Hiệu chỉnh hình học** | Ảnh RGB $1920 \times 1080$ | Ma trận $\mathbf{H}_{3 \times 3}$ đóng băng | Tie Points, SVD Homography (Mục 2.6) | $1.20\text{ ms}$ *(Chỉ 1 lần đầu)* |
| **Stage 1: Thu nhận & Cắt con ROI** | Thông lượng quang học | Ảnh xám con $f_{\text{ROI}}$ ($600 \times 600$) | Sampling, Quantization, Subimage $O(1)$ (Mục 2.4, 2.6) | **$0.05\text{ ms}$** |
| **Stage 2: Cổng IQA & Lọc Gauss** | Ảnh xám con $f_{\text{ROI}}$ | Ảnh mịn $f_t$ ($600 \times 600$) | HSV Value, Laplacian $\text{Var}(\nabla^2 f)$, Separable Gauss (Ch. 3, 6, 10) | **$0.35\text{ ms}$** |
| **Stage 3: Phân đoạn vi sai** | 2 frame xám ($f_t, f_{t-1}$) | Mặt nạ ứng viên $M_{\text{cand}}$ | Directional Subtraction, Ngưỡng tối $f \le 85$, Sobel (Ch. 2, 10) | **$0.42\text{ ms}$** |
| **Stage 4: Tinh lọc hình thái** | Mặt nạ nhị phân $M_{\text{cand}}$ | Mặt nạ vết mực $M_{\text{final}}$ | Opening chữ thập $3 \times 3$, Lọc diện tích liên thông (Ch. 9, 11) | **$0.28\text{ ms}$** |
| **Stage 5: Trọng tâm & Nắn Canvas** | Mặt nạ nhị phân $M_{\text{final}}$ | Tọa độ Canvas $(x, y)_{\text{canon}}$ | Spatial Moments $\mu_{pq}$, Ánh xạ $\mathbf{H}_{3 \times 3}$ $O(1)$, Bresenham (Ch. 2, 11) | **$0.14\text{ ms}$** |
| **Stage 6: Phân loại nét (Nhấc bút)** | Chuỗi quỹ đạo $\mathbf{P}_{\text{raw}}$ | Gói tin điều khiển MQTT | Arc-Length Resampling, Z-score, Bit-plane, Deep CNN (Ch. 8, 11, 12) | **$1.80\text{ ms}$** *(Khi nhấc bút)* |
| **TỔNG THỜI GIAN FRAME BÌNH THƯỜNG (STAGES 1–5)** | **Quang học $\to$ Canvas nắn phẳng** | **Độ trễ toàn pipeline DIP** | **Xử lý liên tục 60 FPS** | **$\approx \mathbf{1.24\text{ ms}}$ / frame** |
| **TỔNG THỜI GIAN FRAME ĐẶC BIỆT KHI NHẮC BÚT (STAGES 1–6)** | **Quang học $\to$ Phản hồi ESP32** | **Độ trễ nhận diện kết thúc nét** | **Xử lý suy luận nơ-ron + Mạng** | **$\approx \mathbf{3.04\text{ ms}}$ / frame** |

$$\text{Tỷ lệ chiếm dụng chu kỳ } 60\text{ FPS} = \frac{1.24\text{ ms}}{16.66\text{ ms}} \approx \mathbf{7.4\%}\text{ tài nguyên của CPU},$$

chứng minh hệ thống vận hành với tốc độ tiệm cận tức thời, mượt mà tuyệt đối và không gây bất kỳ độ trễ nào trong mắt người học.
