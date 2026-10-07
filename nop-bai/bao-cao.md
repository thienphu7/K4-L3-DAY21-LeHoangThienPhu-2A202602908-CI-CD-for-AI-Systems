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

**Lý do:** Cấu hình thứ ba có F1 lớp dương cao nhất, vượt ngưỡng 0.65. Cấu hình thứ nhất có accuracy cao nhất nhưng F1 thấp hơn, nên chọn theo accuracy sẽ bỏ qua chất lượng nhận diện người thu nhập cao. Cấu hình thứ hai có learning_rate và số cây thấp, F1 chỉ đạt 0.6051. Giảm learning_rate thường cần tăng số cây để bù đóng góp của mỗi cây; tuy nhiên, độ sâu cũng thay đổi nên chưa thể quy riêng tác động cho một tham số. MLflow ghi lại ba thí nghiệm.

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập holdout có 124/500 mẫu thu nhập cao, chiếm 24.8%; lớp thu nhập thấp chiếm 75.2%. Mô hình luôn đoán thu nhập thấp vẫn đạt accuracy 75.2%, dù bỏ sót mọi trường hợp thu nhập cao và có F1 lớp dương bằng 0. F1 là trung bình điều hòa của precision và recall, phản ánh dự đoán dương sai và bỏ sót. Pipeline dùng `f1_score(y_eval, preds)` với lớp dương là 1 và chặn triển khai khi F1 dưới 0.65. Không dùng weighted vì lớp đa số có thể che chất lượng lớp dương; macro cho hai lớp trọng số bằng nhau nhưng cũng không đo riêng mục tiêu nhận diện thu nhập cao.

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Không dùng được GCP. | Billing bị chặn. | Chuyển DVC, SDK và credentials sang Azure Blob Storage. |
| MLflow không khởi động được. | Thiếu pkg_resources. | Cài và giữ setuptools dưới phiên bản 81. |
| Release không restart API được. | VM thiếu income-api.service. | Đưa API, cấu hình Azure và systemd lên VM; chạy lại Release thành công. |

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (22.361 mẫu) | 0.714932 | 0.874 |
| Bước 3 (44.722 mẫu) | 0.735426 | 0.882 |

**Nhận xét:** F1 tăng 0.020494 và accuracy tăng 0.008 trên cùng holdout, nhưng thêm dữ liệu không bảo đảm luôn tốt hơn. Commit `319e557` chỉ đổi con trỏ DVC và tự kích hoạt đủ bốn jobs thành công, chứng minh huấn luyện và triển khai lại tự động. Số liệu lấy từ report/log CI của [bước 2](https://github.com/thienphu7/K4-L3-DAY21-LeHoangThienPhu-2A202602908-CI-CD-for-AI-Systems/actions/runs/37635194846) và [bước 3](https://github.com/thienphu7/K4-L3-DAY21-LeHoangThienPhu-2A202602908-CI-CD-for-AI-Systems/actions/runs/37638056986).
