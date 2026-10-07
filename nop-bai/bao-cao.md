# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Lê Hoàng Thiên Phú |
| MSSV | 2A202602908 |
| Lớp / Khóa | K4-L3A |
| Repo GitHub | https://github.com/thienphu7/K4-L3-DAY21-LeHoangThienPhu-2A202602908-CI-CD-for-AI-Systems |
| Ngày nộp | 07/10/2026 |

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Cấu hình ba có F1 cao nhất; cấu hình một có accuracy cao nhất nhưng F1 thấp hơn. Giảm learning_rate thường cần tăng số cây; độ sâu cũng thay đổi nên chưa thể tách riêng tác động từng tham số.

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Holdout có 124/500 mẫu thu nhập cao (24.8%). Luôn đoán thu nhập thấp vẫn đạt accuracy 75.2% nhưng F1 lớp dương bằng 0. F1 kết hợp precision và recall, phản ánh dự đoán dương sai và bỏ sót. Pipeline dùng F1 lớp 1, ngưỡng 0.65. Không dùng weighted vì lớp đa số có thể che chất lượng lớp dương; macro cũng không đo riêng mục tiêu nhận diện thu nhập cao.

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Không dùng được GCP. | Billing bị chặn. | Chuyển DVC, SDK và credentials sang Azure Blob Storage. |
| MLflow không khởi động được. | Thiếu pkg_resources. | Cài và giữ setuptools dưới phiên bản 81. |
| Release không restart API được. | VM thiếu income-api.service. | Đưa API, cấu hình Azure và systemd lên VM; chạy lại Release thành công. |

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (22.361 mẫu) | 0.714932 | 0.874 |
| Bước 3 (44.722 mẫu) | 0.735426 | 0.882 |

**Nhận xét:** F1 tăng 0.020494, accuracy tăng 0.008; thêm dữ liệu không bảo đảm luôn tốt hơn. Commit `319e557` chỉ đổi DVC pointer và tự kích hoạt đủ bốn jobs xanh. Hai report CI gốc được lưu trong `nop-bai/report-buoc-2.json` và `report-buoc-3.json`.

## 5. Phần Bonus Đã Thực Hiện

- Bonus 1: Actions ghi parameters, metrics, model lên DagsHub; ảnh 06 là bằng chứng.
- Bonus 2: Quét 0.1–0.9, bước 0.05; ngưỡng 0.30 nâng F1 0.735426 lên 0.753731, accuracy 0.868; API dùng ngưỡng lưu cùng model. Chọn trên holdout nên chưa phải đánh giá độc lập.
- Bonus 3: detail.txt có confusion matrix, precision/recall từng lớp. Lớp dương: precision 0.701389, recall 0.814516; nếu tìm khách hàng, bỏ sót mất cơ hội nên ưu tiên recall hơn chi phí tiếp cận nhầm.
- Bonus 4: So F1 với report Azure trước deploy; thử candidate 0.725426 bị chặn, model cũ giữ nguyên; lưu model/report theo phiên bản.
- Bonus 5: Tỷ lệ dương 24.7842%, lệch dưới 5 điểm phần trăm so với 24.8%; dữ liệu giả 50% phát cảnh báo.
