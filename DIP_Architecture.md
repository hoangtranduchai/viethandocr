# KHUNG KIẾN TRÚC TỔNG QUÁT PHÂN HỆ XỬ LÝ ẢNH SỐ (DIGITAL IMAGE PROCESSING)
## DỰ ÁN TRỢ LÝ LUYỆN VIẾT CHỮ KANJI THỜI GIAN THỰC (60 FPS)

---

Khung kiến trúc tổng quát của phân hệ **Xử lý Ảnh số (Digital Image Processing - DIP)** cho toàn bộ dự án trợ lý luyện viết chữ Kanji được thiết lập chuẩn xác $100\%$ dựa trên sự tích hợp toàn diện ba trụ cột lý luận cốt lõi trong giáo trình *Digital Image Processing, 4th Edition* (Rafael C. Gonzalez & Richard E. Woods):
1. **Mục 1.1:** Mô hình tiến trình liên tục 3 cấp độ (*Low-level, Mid-level, High-level Processes*).
2. **Mục 1.4 & Hình 1.23:** 10 khối chức năng cơ bản và Cơ sở tri thức trung tâm (*Knowledge Base*).
3. **Mục 1.5 & Hình 1.24:** Hệ thống phần cứng và hạ tầng tính toán số hóa (*Components of an Image Processing System*).

Kiến trúc này giải quyết triệt để bài toán thời gian thực $60\text{ FPS}$ (ngân sách chu kỳ $\le 16.66\text{ ms}$ cho mỗi khung hình), kiểm soát hiện tượng bóng đổ bàn tay và che khuất ngòi bút mà không cần bất kỳ phụ kiện cảm ứng nào gắn trên người học.

---

### SƠ ĐỒ TOÀN CẢNH KIẾN TRÚC TỔNG QUÁT (CHUẨN HÌNH 1.23 & HÌNH 1.24 DIP 4E)

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                    TOÀN BỘ KHUNG KIẾN TRÚC TỔNG QUÁT PHÂN HỆ XỬ LÝ ẢNH SỐ (CHUẨN DIP 4E)                               │
 ├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                                                        │
 │  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
 │  │                       NHÓM 1: ĐẦU RA LÀ ẢNH (Outputs of these processes generally are images)                    │  │
 │  └─────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘  │
 │                                                            │                                                           │
 │  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────┴─────┐   ┌─────────────────┐   ┌───────────────────────┐   │
 │  │    CHAPTER 6    │   │    CHAPTER 7    │   │     CHAPTER 8     │   │    CHAPTER 9    │   │       CHAPTER 5       │   │
 │  │   Color Image   │   │  Wavelets and   │   │    Compression    │   │  Morphological  │   │   Image Restoration   │   │
 │  │   Processing    │   │ Other Transforms│   │                   │   │   Processing    │   │                       │   │
 │  │ • Đo kênh sáng  │   │ • Biểu diễn đa  │   │ • Nén không tổn   │   │ • Lọc cấu trúc  │   │ • Nắn phối cảnh       │   │
 │  │   V trong HSV   │   │   tỉ lệ Pyramid │   │   hao Bit-plane   │   │   ô ly giấy viết│   │   Homography H_3x3    │   │
 │  │   phục vụ IQA   │   │   đối soát cỡ   │   │   cho Canvas nhị  │   │ • Lọc bỏ mảng   │   │   đưa về hệ tọa độ    │   │
 │  │   (Mục 6.2)     │   │   chữ (Mục 7.1) │   │   phân (Mục 8.2)  │   │   bụi rác (Ch.9)│   │   128x128 px (Mục 2.6)│   │
 │  └────────▲────────┘   └────────▲────────┘   └─────────▲─────────┘   └────────▲────────┘   └───────────▲───────────┘   │
 │           │ ↕                   │ ↕                    │ ↕                    │ ↕                      │ ↕             │
 │  ┌────────┴─────────────────────┴──────────────────────┴──────────────────────┴────────────────────────┴────────────┐  │
 │  │                                                                                                                  │  │
 │  │                                        KNOWLEDGE BASE (CƠ SỞ TRI THỨC TRUNG TÂM)                                 │  │
 │  │ • Tri thức 512 chữ Kanji Look and Learn (16 nhóm bộ thủ A–P, 6 quy tắc bút thuận sư phạm cơ bản).                │  │
 │  │ • Bảng thông số vật lý định lượng: Ngưỡng phản xạ mực T_ink ≤ 85, Var(∇²f) ≥ 65, Gradient Sobel ≥ 30.            │  │
 │  │ • Ràng buộc quan hệ hình học các cặp chữ dị biệt (đâm xuyên, tỉ lệ dài/ngắn: 土/士, 午/牛, 未/末).                │  │
 │  │ • Cơ chế tương tác hai chiều (Double-headed arrows ↕): Áp đặt luật kiểm soát và nhận dữ liệu thống kê cập nhật.   │  │
 │  │                                                                                                                  │  │
 │  └────────▲─────────────────────┬──────────────────────┬──────────────────────┬────────────────────────▲────────────┘  │
 │           │ ↕                   │ ↕                    │ ↕                    │ ↕                      │ ↕             │
 │  ┌────────┴────────┐   ┌────────┴────────┐   ┌─────────┴─────────┐   ┌────────┴────────┐   ┌───────────┴───────────┐   │
 │  │ CHAPTERS 3 & 4  │   │   CHAPTER 10    │   │    CHAPTER 11     │   │   CHAPTER 12    │   │       CHAPTER 2       │   │
 │  │ Image Filtering │   │  Segmentation   │   │ Feature Extraction│   │ Pattern Classif.│   │   Image Acquisition   │   │
 │  │  & Enhancement  │   │                 │   │                   │   │                 │   │                       │   │
 │  │ • Cổng IQA vi   │   │ • Trừ vi sai có │   │ • Rút trích trọng │   │ • Deep CNN nhận │   │ • Thu nhận luồng thô  │   │
 │  │   phân Laplace  │   │   hướng Δ_t     │   │   tâm ngòi bút    │   │   diện 8 loại   │   │   1080p@60FPS         │   │
 │  │   ngắt frame mờ │   │ • Cắt ngưỡng độ │   │   qua Moment μ_pq │   │   nét cơ bản    │   │ • Khóa cứng thông số  │   │
 │  │ • Lọc không gian│   │   tối f_t ≤ 85  │   │ • Tái lấy mẫu đẳng│   │ • So khớp Cây   │   │   Focus & Exposure    │   │
 │  │   Gaussian 3x3  │   │ • Gradient Sobel│   │   cự 32 điểm      │   │   Trie 512 chữ  │   │ • Cắt ma trận con ROI │   │
 │  │   khử nhiễu     │   │   kháng bóng tay│   │   chuẩn hóa Z-scor│   │   bắt lỗi sai   │   │   600x600 px          │   │
 │  └─────────────────┘   └─────────────────┘   └───────────────────┘   └─────────────────┘   └───────────▲───────────┘   │
 │                                                                                                        │               │
 │                                                                                                [Problem Domain]        │
 │                                                                                                • Bàn học, giấy trắng   │
 │                                                                                                • Bút mực, bóng bàn tay │
 │                                                                                                                        │
 │  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
 │  │                     NHÓM 2: ĐẦU RA LÀ THUỘC TÍNH ẢNH (Outputs of these processes are image attributes)            │  │
 │  └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1. Phân Rã Bản Chất 3 Cấp Độ Xử Lý Trong Hệ Thống (DIP Mục 1.1)

Tiến trình xử lý liên tục được tổ chức nghiêm ngặt thành 3 cấp độ dựa trên bản chất cấu trúc dữ liệu ở đầu vào và đầu ra:

* **Cấp độ 1: Xử lý Mức thấp (Low-Level Processes):**
  * *Bản chất toán học:* Ánh xạ ma trận sang ma trận $f(x, y) \to g(x, y)$.
  * *Tập hợp module thực thi:* Chapter 2 (Acquisition), Chapter 3 & 4 (Filtering/Enhancement), Chapter 5 (Restoration), Chapter 6 (Color), Chapter 7 (Wavelets/Transforms), Chapter 8 (Compression).
  * *Nhiệm vụ trong dự án:* Đón nhận tín hiệu quang thông vật lý, chuyển đổi thành ma trận số 8-bit $f(x, y) \in [0, 255]$. Cắt ngay vùng ảnh con ROI $600 \times 600\text{ px}$ bằng kỹ thuật trỏ mảng $O(1)$. Đo độ sắc nét Laplacian $\text{Var}(\nabla^2 f)$ để ngắt sớm frame hỏng, làm mịn Gaussian $3 \times 3$ khử nhiễu cảm biến, và áp dụng ma trận Homography $\mathbf{H}_{3 \times 3}$ nắn phối cảnh về Canvas chuẩn $128 \times 128\text{ px}$. Toàn bộ dữ liệu sau các khâu này vẫn duy trì ở dạng ma trận điểm ảnh.

* **Cấp độ 2: Xử lý Mức trung bình (Mid-Level Processes):**
  * *Bản chất toán học:* Ánh xạ ma trận ảnh sang không gian vector thuộc tính $g(x, y) \to \mathbf{x} \in \mathbb{R}^k$.
  * *Tập hợp module thực thi:* Chapter 9 (Morphology), Chapter 10 (Segmentation), Chapter 11 (Feature Extraction).
  * *Nhiệm vụ trong dự án:* Phân đoạn vết mực bằng phép trừ vi sai thời gian có hướng kết hợp cổng độ tối tuyệt đối ($f_t \le 85$) và gradient biên vi phân Sobel ($\Vert\nabla f_t\Vert \ge 30$). Áp dụng toán tử hình thái học Opening và lọc diện tích thành phần liên thông $[4, 150]\text{ px}$ để triệt tiêu nhiễu rác. Rút trích tọa độ trọng tâm ngòi bút $(x_t, y_t)$ thông qua các Moment không gian bậc 0 và 1 ($\mu_{00}, \mu_{10}, \mu_{01}$), sau đó tham số hóa quỹ đạo động học thành vector chuỗi 32 điểm đẳng cự.

* **Cấp độ 3: Xử lý Mức cao (High-Level Processes):**
  * *Bản chất toán học:* Ánh xạ vector thuộc tính sang nhãn nhận thức ngữ nghĩa $\mathbf{x} \to \omega_j \in \Omega$.
  * *Tập hợp module thực thi:* Chapter 12 (Pattern Classification) kết hợp Module Đối soát Tri thức.
  * *Nhiệm vụ trong dự án:* Thực hiện các chức năng nhận thức (Cognitive Functions) mô phỏng thị giác con người: Sử dụng Mạng nơ-ron tích chập sâu (Deep CNN) để gán nhãn cho 8 loại nét cơ bản (Ngang, Sổ, Phẩy, Mác, Hất, Gập, Móc, Chấm). Truy vấn Cây tiền tố (Prefix Trie) chứa tri thức 512 chữ Kanji để thẩm định trật tự bút thuận và các quy tắc cấu trúc hình học (đâm xuyên, tỉ lệ dài ngắn), từ đó phát lệnh điều khiển phần cứng.

---

### 2. Phân Nhóm Đầu Ra & Vai Trò Bản Lề Của Hình Thái Học (DIP Hình 1.23)

Hình 1.23 trong sách phân định rõ ràng hai nhóm đầu ra:

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │ NHÓM 1: ĐẦU RA LÀ ẢNH (Outputs are images):                                            │
 │ • Ch 2 (Acquisition) ──> Ch 3 & 4 (Filtering/Enhancement) ──> Ch 5 (Restoration)       │
 │ • Ch 6 (Color) ──> Ch 7 (Transforms) ──> Ch 8 (Compression) ──> Ch 9 (Morphology)      │
 ├────────────────────────────────────────────────────────────────────────────────────────┤
 │ NHÓM 2: ĐẦU RA LÀ THUỘC TÍNH (Outputs are attributes):                                 │
 │ • Ch 9 (Morphology) ──> Ch 10 (Segmentation) ──> Ch 11 (Feature) ──> Ch 12 (Class.)    │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

> **Điểm giao thoa cốt lõi (Bridge):** **Chapter 9 (Morphological Processing)** là khối duy nhất nằm đồng thời ở cả hai nhóm. Phép toán mở hình thái học ($A \circ B = (A \ominus B) \oplus B$) sử dụng phần tử cấu trúc $B$ để bóc tách nhiễu, xuất ra ma trận ảnh nhị phân sạch (thuộc Nhóm 1). Ngay sau đó, thuật toán trích xuất thành phần liên thông (Connected Components) tính toán trực tiếp các đại lượng hình học số học như diện tích (Area), chu vi và khung xương của nét viết để chuyển giao sang Nhóm 2.

---

### 3. Phân Rã Nhiệm Vụ 10 Khối Xử Lý Chuyên Biệt Theo DIP 4E

Tất cả 10 khối trong Hình 1.23 được phân bổ nhiệm vụ toán học rõ ràng để hiện thực hóa bài toán luyện viết Kanji:

* **Problem Domain (Miền bài toán thực tế):**
  * Không gian vật lý nơi người học ngồi viết tự nhiên: Mặt bàn học, tờ giấy viết kẻ ô ly, cây bút thông thường, ánh sáng đèn bàn và bóng bàn tay cử động liên tục.

* **Khối 1 (Chapter 2) — Image Acquisition (Thu nhận ảnh):**
  * Nhận tín hiệu từ mảng cảm biến 2 chiều (CCD/CMOS Array Sensor - Mục 2.3) ở tốc độ $1080\text{p} @ 60\text{ FPS}$.
  * Thực hiện số hóa tín hiệu: Lấy mẫu không gian (Sampling) trên lưới tọa độ $\mathbb{Z}^2$ và lượng tử hóa cường độ biên độ (Quantization) thành các mức xám số nguyên $l \in [0, 255]$ ($k = 8\text{ bits}$) theo Mục 2.4.
  * Khóa cứng thông số lấy nét và phơi sáng (`Focus Lock` & `Exposure Lock`) để triệt tiêu hiện tượng nhấp nháy quang học.
  * Trích xuất ma trận con ROI (Subimage Extraction - Mục 2.6) thu hẹp phạm vi xử lý từ $1920 \times 1080$ xuống $600 \times 600\text{ px}$ bằng kỹ thuật trỏ ô nhớ $O(1)$, giảm tải tính toán $5.76\text{ lần}$.

* **Khối 2 (Chapters 3 & 4) — Image Filtering and Enhancement (Lọc không gian & Tăng cường):**
  * *Chương 3 (Miền không gian):* Áp dụng toán tử vi phân bậc hai Laplacian rời rạc $3 \times 3$ ($\nabla^2 f$) trên vùng ROI để tính phương sai $\text{Var}(\nabla^2 f)$ làm Cổng IQA (Mục 3.6 & 10.2). Khung hình có $\text{Var}(\nabla^2 f) < 65.0$ (bị mờ do rung bàn) sẽ bị hủy bỏ ngay lập tức nhằm tiết kiệm tài nguyên.
  * Áp dụng mặt nạ lọc không gian làm mịn Gaussian tách rời (Separable Kernel - Mục 3.5) kích thước $3 \times 3$ với $\sigma = 0.8$ để triệt tiêu nhiễu cộng ngẫu nhiên $\eta(x, y)$ của cảm biến trước khi tính toán vi sai.
  * *Chương 4 (Miền tần số):* Định hình nền tảng lọc thông thấp, hiểu rõ cơ chế suy hao tần số cao khi ảnh bị rung nhòe.

* **Khối 3 (Chapter 5) — Image Restoration (Khôi phục & Hiệu chỉnh hình học):**
  * Bù trừ biến dạng suy thoái phối cảnh (Perspective Distortion) do camera đặt ở góc nghiêng tự do $45^\circ\text{--}60^\circ$ trên giá đỡ.
  * Dựa trên 4 điểm neo (Tie Points / Reseau Marks - Mục 2.6 & Chương 5) tại 4 góc của ô viết, giải hệ phương trình tuyến tính tìm ma trận Homography $\mathbf{H}_{3 \times 3}$ và lưu cố định vào RAM Cache.
  * Ánh xạ tức thời tọa độ điểm viết $(x_t, y_t)$ về Canvas chuẩn $128 \times 128\text{ px}$ với độ phức tạp $O(1)$ tiêu tốn chỉ $0.02\text{ ms}$.

* **Khối 4 (Chapter 6) — Color Image Processing (Xử lý ảnh màu):**
  * Chuyển đổi ma trận RGB sang không gian màu HSV để bóc tách độc lập kênh độ sáng $V$ (Value) theo Mục 6.2.
  * Đo độ rọi trung bình $\bar{V}$ phục vụ Cổng kiểm soát quang học ($40 \le \bar{V} \le 235$) nhằm phát hiện tình trạng thiếu sáng hoặc lóa bề mặt (Specular Reflection).

* **Khối 5 (Chapter 7) — Wavelets and Other Transforms (Biến đổi đa tỉ lệ):**
  * Biểu diễn cấu trúc nét chữ dưới dạng kim tự tháp đa phân giải (Pyramidal Representation - Mục 7.1) khi cần đối soát cấu trúc chữ tổng thể độc lập với kích cỡ viết to hay nhỏ của người học.

* **Khối 6 (Chapter 8) — Image Compression (Nén dữ liệu ảnh):**
  * Áp dụng nén mặt phẳng bit (Bit-plane / Bit-packing - Mục 8.2) trên ma trận Canvas nhị phân $128 \times 128\text{ px}$.
  * Nén ma trận $16.384\text{ bytes}$ thô thành gói tin $2.048\text{ bytes}$ để truyền qua mạng nội bộ LAN xuống trạm ESP32 trong thời gian $< 1\text{ ms}$.

* **Khối 7 (Chapter 9) — Morphological Processing (Xử lý hình thái học):**
  * Áp dụng toán tử mở (Opening: $A \circ B = (A \ominus B) \oplus B$) với phần tử cấu trúc chữ thập $3 \times 3$ để khử các chấm nhiễu cô lập.
  * Phân tích các thành phần liên thông (Connected Components - Mục 9.5) và lọc diện tích: Loại bỏ toàn bộ các mảng có $\text{Area} \notin [4, 150]\text{ px}$ để triệt tiêu nhiễu bóng tay hoặc mép quần áo.

* **Khối 8 (Chapter 10) — Image Segmentation (Phân đoạn vết mực vi sai):**
  * Thực hiện phân đoạn chuyển động (The Use of Motion in Segmentation - Mục 10.6) bằng phép trừ vi sai thời gian có hướng:
    $$\Delta_t(x, y) = \max\Big(0, f_{t-1}(x, y) - f_t(x, y)\Big)$$
    để chỉ phát hiện các điểm ảnh chuyển từ sáng sang tối (vết mực mới xuất hiện).
  * Áp dụng Cổng độ tối tuyệt đối $f_t(x, y) \le 85$ dựa trên mô hình phản xạ $f = i \cdot r$ (Mục 2.3) để loại bỏ hoàn toàn vùng bóng tay xám ($f \approx 130\text{--}170$).
  * Tính độ dốc biên vi phân Sobel $\Vert\nabla f_t\Vert \ge 30$ (Mục 10.2) để lọc bỏ viền bóng mờ và chỉ giữ lại bờ sắc nét của vệt mực thật.

* **Khối 9 (Chapter 11) — Feature Extraction (Trích xuất đặc trưng):**
  * *Mô tả vùng (Region Descriptors):* Tính các Moment không gian bậc 0 và 1 ($\mu_{00}, \mu_{10}, \mu_{01}$) theo Mục 11.3 để xác định chính xác tọa độ trọng tâm $(x_t, y_t) = (\mu_{10}/\mu_{00}, \mu_{01}/\mu_{00})$ của giọt mực vi sai mới xuất hiện ở mép sau ngón tay.
  * *Mô tả biên & đường (Boundary Descriptors):* Khi người học nhấc bút, chuỗi điểm được tham số hóa theo độ dài cung tích lũy $s_k$ (Mục 11.1) và tái lấy mẫu đẳng cự thành đúng $32\text{ mốc}$ không gian phân bố đều. Chuẩn hóa thống kê Z-Score kết hợp đạo hàm vận tốc $(\Delta x_i, \Delta y_i, \Delta t_i)$ tạo thành Tensor đặc trưng $[1, 32, 5]$.

* **Khối 10 (Chapter 12) — Image Pattern Classification (Phân loại mẫu nét):**
  * Nạp song song Tensor đặc trưng và Canvas nhị phân vào mạng nơ-ron tích chập sâu (Deep CNN - Mục 12.5) để nhận dạng và phân loại chính xác 8 loại nét cơ bản chữ Hán.
  * Đối soát thứ tự nét với Cây tiền tố (Prefix Trie) chứa tri thức 512 chữ Kanji để phát hiện lỗi sai tức thì ($O(1)$).

---

### 4. Cơ Sở Tri Thức Trung Tâm (Knowledge Base) & Tương Tác Hai Chiều ($\leftrightarrow$)

Khối **Knowledge Base** là bộ não trung tâm của sơ đồ Hình 1.23, duy trì tương tác hai chiều thông qua các mũi tên đối xứng ($\leftrightarrow$) với tất cả các module xử lý:

```text
       ┌───────────────────────────────┐                  ┌──────────────────────────────────────────────┐
       │   CÁC MODULE XỬ LÝ (CH 2-12)  │                  │         KNOWLEDGE BASE (CƠ SỞ TRI THỨC)      │
       │                               │ ───────────────> │ • 512 Kanji Look and Learn (Bộ thủ A-P)      │
       │ • Thu nhận, Lọc, Phân đoạn,   │   (Cập nhật      │ • 6 quy tắc bút thuận sư phạm                │
       │   Trích xuất đặc trưng        │    thống kê)     │ • Bảng thông số vật lý & ngưỡng quang học    │
       │                               │ <─────────────── │ • Ràng buộc hình học phân biệt chữ dị biệt   │
       └───────────────────────────────┘   (Áp đặt luật   └──────────────────────────────────────────────┘
                                            và giới hạn)
```

* **Tác động kiểm soát xuôi ($\text{Knowledge} \to \text{Modules}$):**
  * *Thu hẹp không gian tìm kiếm (Search Space Limitation):* Knowledge Base cung cấp thông tin tiên nghiệm (*A priori Information*) về vị trí ô viết và các ngưỡng vật lý định lượng ($T_{\text{ink}} \le 85$, diện tích ngòi bút $4\text{--}150\text{ px}$). Các thuật toán ở Chapter 10 và 11 không phải quét mù quáng trên toàn bộ không gian ảnh, giảm tối đa độ phức tạp thuật toán.
  * *Áp đặt quy tắc sư phạm:* Quy định trước loại nét và hướng nét hợp lệ kế tiếp theo 6 quy tắc bút thuận chữ Hán (Trên trước dưới sau, Trái trước phải sau, Ngang trước sổ sau...).

* **Tác động thích nghi ngược ($\text{Modules} \to \text{Knowledge}$):**
  * Các tham số thống kê đo đạc thực tế (độ rọi phòng $\bar{V}$ từ Chương 6, mức xám nền trang giấy từ Chương 3) được gửi ngược về Knowledge Base để cập nhật các ngưỡng phân đoạn thích nghi theo thời gian thực.

* **Cơ chế ngắt khẩn cấp (Circuit-Breaker):**
  * Nếu Cổng IQA ở Khối 2 đo được $\text{Var}(\nabla^2 f) < 65.0$, Knowledge Base lập tức phát tín hiệu ngắt toàn bộ tiến trình phía sau, dừng mọi tính toán phân đoạn vi sai và mạng nơ-ron để bảo vệ CPU khỏi tình trạng quá tải.

---

### 5. Cấu Trúc Phần Cứng Hệ Thống (Mục 1.5 & Hình 1.24 DIP 4E)

Mô hình triển khai phần cứng bám sát sơ đồ phân rã linh kiện tại Hình 1.24 của giáo trình:

```text
 ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                      CẤU TRÚC PHẦN CỨNG HỆ THỐNG THEO HÌNH 1.24 DIP 4E                                     │
 ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                                             │
 │  [Problem Domain] ──> [Image Sensors & Digitizer] ──(Cáp USB Type-C)──> [Computer (Laptop CPU Edge AI)]    │
 │   (Bàn học, Vở, Bút)    (Camera CMOS 1080p@60FPS)                         │ (Zero-Allocation Pipeline)      │
 │                                                                           │                                 │
 │                                                   ┌───────────────────────┴───────────────────────┐         │
 │                                                   ▼ (Giao tiếp Wi-Fi LAN - Độ trễ < 1ms)          ▼         │
 │                                            [Network/Cloud]                             [Mass Storage]       │
 │                                            (Mạng nội bộ LAN)                           (RAM Buffer Cache)   │
 │                                                   │                                                         │
 │                                                   ▼                                                         │
 │                                     [Image Displays & Hardcopy]                                             │
 │                                     (Trạm để bàn ESP32: OLED 0.96", LED Xanh/Đỏ, Còi Buzzer)                │
 └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

* **Image Sensors & Digitizer:** Cảm biến CMOS trên điện thoại kết hợp bộ số hóa phần cứng truyền luồng dữ liệu liên tục qua cáp USB Type-C với băng thông ổn định, đáp ứng tốc độ khung hình cao ($60\text{ FPS}$).
* **Computer (Laptop Edge-AI):** Máy tính xử lý trung tâm (*General-purpose Computer*), thực thi toàn bộ pipeline DIP bằng kỹ thuật cấp phát bộ nhớ tĩnh (*Zero-Allocation Paradigm*) để ngăn hiện tượng phân mảnh bộ nhớ và khựng hình do bộ gom rác.
* **Network & Displays (Trạm ESP32 để bàn):** Mạng nội bộ chuyên dụng (*Dedicated Local Network*) truyền các gói tin JSON điều khiển qua giao thức MQTT xuống trạm để bàn ESP32 gồm màn hình OLED $0.96''$, đèn LED và còi buzzer để phản hồi trong vòng chưa đầy $15\text{ ms}$.

---

### 6. Bảng Phân Bổ Thời Gian Xử Lý (Latency Budget) Chuẩn $60\text{ FPS}$

Chu kỳ tối đa cho mỗi khung hình ở $60\text{ FPS}$ là **$16.66\text{ ms}$**. Dưới đây là bảng phân bổ thời gian thực thi trên CPU Laptop:

| Giai Đoạn Xử Lý Trong Khung Kiến Trúc DIP 4E | Phương Trình / Thuật Toán Toán Học Cốt Lõi | Thời Gian Thực Thi (CPU Laptop) |
| :--- | :--- | :--- |
| **Khối 1: Cắt ảnh con ROI $600 \times 600\text{ px}$ (Ch 2)** | $f_{\text{ROI}} = f_{\text{full}}[y_{\min}:y_{\max},\; x_{\min}:x_{\max}]$ (Trỏ mảng $O(1)$) | **$0.05\text{ ms}$** |
| **Khối 2: Cổng IQA Laplacian + Lọc Gauss $3 \times 3$ (Ch 3, 10)** | $\text{Var}(\nabla^2 f) \ge 65.0$ & Tích chập Gaussian tách rời $\sigma = 0.8$ | **$0.35\text{ ms}$** |
| **Khối 8: Trừ vi sai + Cắt ngưỡng tối + Sobel (Ch 10)** | $\Delta_t = \max(0, f_{t-1} - f_t) \cap (f_t \le 85) \cap (\Vert\nabla f_t\Vert \ge 30)$ | **$0.42\text{ ms}$** |
| **Khối 7: Lọc hình thái Opening & Diện tích (Ch 9)** | $(M_{\text{cand}} \circ B) \cap (\text{Area} \in [4, 150]\text{ px})$ | **$0.28\text{ ms}$** |
| **Khối 9: Trích xuất Moments ngòi bút (Ch 11)** | $\mu_{00} = \sum M(x, y),\; x_t = \mu_{10}/\mu_{00},\; y_t = \mu_{01}/\mu_{00}$ | **$0.12\text{ ms}$** |
| **Khối 3: Nắn phẳng Homography $\mathbf{H}_{3 \times 3}$ (Ch 2, 5)** | $[x', y', 1]^T \sim \mathbf{H}_{3 \times 3} \cdot [x_t, y_t, 1]^T$ (Ánh xạ $O(1)$) | **$0.02\text{ ms}$** |
| **Khối 6: Đóng gói nén Canvas nhị phân (Ch 8)** | Bit-packing ma trận nhị phân $128 \times 128\text{ px} \to 2.048\text{ bytes}$ | **$0.08\text{ ms}$** |
| **Khối 10: Deep CNN phân loại nét (Ch 12)** | Suy luận ONNX INT8 (Chỉ kích hoạt khi nhấc bút) | **$1.80\text{ ms}$** *(Khi nhấc bút)* |
| **TỔNG THỜI GIAN PIPELINE TRONG KHUNG HÌNH BÌNH THƯỜNG** | **Toàn bộ chuỗi xử lý DIP thời gian thực** | **$\approx 1.32\text{ ms}$ / khung hình** |
| **TỔNG THỜI GIAN KHUNG HÌNH ĐẶC BIỆT KHI CÓ NHẬN DIỆN NÉT** | **Bao gồm cả mạng nơ-ron Deep CNN** | **$\approx 3.12\text{ ms}$ / khung hình** |

$$\text{Tỷ lệ chiếm dụng tài nguyên CPU} = \frac{1.32\text{ ms}}{16.66\text{ ms}} \approx \mathbf{7.9\%}\text{ ngân sách chu kỳ khung hình},$$

đảm bảo hệ thống đạt độ trễ cực thấp và đáp ứng vận hành thời gian thực $60\text{ FPS}$.
