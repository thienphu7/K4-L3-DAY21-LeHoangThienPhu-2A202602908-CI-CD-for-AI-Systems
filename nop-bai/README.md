# Nộp Bài - Day 21: CI/CD cho AI Systems

Thư mục này là nơi chứa **bằng chứng nộp bài**. Bạn không cần tạo thêm thư mục nào khác:
điền vào các file có sẵn và bỏ ảnh chụp màn hình vào đúng tên file đã quy định.

```
nop-bai/
├── README.md                  <- file này (checklist)
├── bao-cao.md                 <- template báo cáo, không quá 1 trang A4
└── anh-chup-man-hinh/
    ├── README.md              <- mô tả yêu cầu của từng ảnh
    ├── 01-mlflow-ui.png
    ├── 02-actions-buoc-2.png
    ├── 03-actions-buoc-3.png
    ├── 04-curl-api.png
    └── 05-cloud-storage.png
```

---

## Checklist Trước Khi Nộp

Đánh dấu `[x]` khi hoàn thành từng mục:

- [x] Repo GitHub ở chế độ **public** và chứa toàn bộ code, cấu hình đã hoàn thiện.
- [x] Đủ 5 ảnh trong `anh-chup-man-hinh/`, đúng tên file, đúng thứ tự (xem
      [yêu cầu chi tiết](anh-chup-man-hinh/README.md)).
- [x] `bao-cao.md` đã điền đủ 4 mục bắt buộc và không vượt quá 1 trang A4.
- [x] Đã `git push` toàn bộ thư mục `nop-bai/` lên GitHub.
- [ ] Dán URL repo GitHub vào bài nộp trên **https://vlearn.dev**.
- [ ] Mở lại URL vừa nộp ở chế độ ẩn danh để chắc chắn repo public và người chấm xem được.

---

## Ảnh Chụp Màn Hình Tương Ứng Với Rubric

| Ảnh | Chứng minh hạng mục nào trong rubric | Điểm |
|---|---|---|
| `01-mlflow-ui.png` | Bước 1 - MLflow tracking, Bước 1 - Độ đo | 20 |
| `02-actions-buoc-2.png` | Bước 2 - CI/CD (bốn jobs màu xanh) | 16 |
| `03-actions-buoc-3.png` | Bước 3 - Tự động hóa | 12 |
| `04-curl-api.png` | Bước 2 - Serving | 12 |
| `05-cloud-storage.png` | Bước 2 - DVC | 12 |

Phần `bao-cao.md` chứng minh hạng mục **Bước 1 - Phân tích** (4 điểm) và là nơi bạn giải
trình khi một ảnh nào đó chưa thể hiện đủ (ví dụ quality gate đã chặn đúng một lần).

---

## Quy Ước Chung

- **Định dạng ảnh**: `.png` (ưu tiên) hoặc `.jpg`. Nếu dùng `.jpg`, giữ nguyên phần tên,
  chỉ đổi đuôi — ví dụ `01-mlflow-ui.jpg`.
- **Không đổi số thứ tự đầu tên file.** Thứ tự này là thứ tự chấm bài.
- **Không che thông tin cần chấm**: tên job, trạng thái màu xanh, giá trị `f1_score`,
  đường dẫn bucket. Được phép che email cá nhân và khóa bí mật.
- **Cần chụp cả URL trên thanh địa chỉ** với các ảnh chụp từ trình duyệt (MLflow UI,
  GitHub Actions, Cloud Storage Console) để xác nhận đúng repo/project của bạn.
- **Tuyệt đối không commit khóa bí mật**: `sa-key.json`, nội dung GitHub Secrets, access
  key của cloud. Nếu ảnh lỡ chứa các thông tin này, hãy che lại trước khi commit.

---

## Ghi Chú Về Kích Thước Repo

Ảnh chụp màn hình được commit trực tiếp vào Git. Giữ mỗi ảnh dưới **1 MB** (chụp vùng cần
thiết thay vì toàn màn hình 4K, hoặc nén lại trước khi commit) để repo không phình to.

Nếu bạn dùng macOS, có thể nén nhanh bằng lệnh sẵn có:

```bash
sips -Z 1600 nop-bai/anh-chup-man-hinh/01-mlflow-ui.png
```

## Đối chiếu bằng chứng ngày 07/10/2026

- Bước 2: run [37635194846](https://github.com/thienphu7/K4-L3-DAY21-LeHoangThienPhu-2A202602908-CI-CD-for-AI-Systems/actions/runs/37635194846) thành công sau khi bổ sung systemd và chạy lại Release. `report-buoc-2.json` được giải nén từ artifact người học tải về và đối chiếu log Train.
- Bước 3: run [37638056986](https://github.com/thienphu7/K4-L3-DAY21-LeHoangThienPhu-2A202602908-CI-CD-for-AI-Systems/actions/runs/37638056986) có event `push`, commit `319e557` chỉ thay `data/train_batch1.csv.dvc`; cả bốn jobs thành công. `report-buoc-3.json` chép nguyên hai giá trị từ report in trong log Train, job `112849899023`.
- Ảnh Storage dùng hai file `05a-storage-dvc.png` và `05b-storage-model.png` theo quy định trong README ảnh. Đã có đủ hai ảnh Storage; tổng cộng 6 file ảnh cho 5 nhóm bằng chứng.
- Ảnh MLflow có ba bộ tham số, F1 và accuracy, đã sắp theo F1; thiếu thanh URL, giữ nguyên theo yêu cầu người học.
- DVC pointer khớp nội dung cả ba CSV; tập train hiện có 44.722 mẫu, holdout 500 mẫu. API công khai trả health OK và dự đoán hợp lệ sau bước 3.
- Chưa xác nhận nộp URL trên vlearn.dev hoặc kiểm tra ẩn danh; không đánh dấu các mục này thay người học.

## Bonus 1 — DagsHub

Workflow run [37640663189](https://github.com/thienphu7/K4-L3-DAY21-LeHoangThienPhu-2A202602908-CI-CD-for-AI-Systems/actions/runs/37640663189) ghi thí nghiệm vào DagsHub. API MLflow xác nhận run `6596fe89bd794567954c8cd9c39f1df2` có trạng thái FINISHED, F1 0.7354260089686099, accuracy 0.882 và tag commit `51f02a5`. Artifact store dùng `mlflow-artifacts:` của server. Chụp giao diện DagsHub thấy run, parameters và metrics, lưu `anh-chup-man-hinh/06-dagshub-mlflow.png` để bổ sung bằng chứng bonus.

## Bonus 2–5 — Cách kiểm chứng

- `src/train.py`: quét 17 ngưỡng từ 0.10 đến 0.90, log ngưỡng/F1 mặc định/tỷ lệ dương lên MLflow và lưu report. Thuộc tính `income_threshold_` đi cùng file model để API dùng đúng ngưỡng. F1 đã tối ưu trên holdout không phải đánh giá độc lập.
- `src/detail.py`: workflow chạy sau Train để tạo `outputs/detail.txt`, gồm confusion matrix và precision/recall từng lớp; artifact `report` chứa cả JSON và TXT.
- `src/release.py`: so F1 với `artifacts/current/report.json`, chỉ publish nếu không giảm; báo lỗi khi baseline không hợp lệ hoặc hash model/report không khớp. Report/model được lưu cả dưới `artifacts/versions/<run-id>-<attempt>/`. Khi candidate bị chặn, bước copy API và restart được skip.
- Tỷ lệ dương tham chiếu 0.248, cảnh báo nếu chênh lệch lớn hơn 0.05; dữ liệu lệch chỉ cảnh báo, không làm pipeline thất bại.
- `bonus-guard-checks.txt` ghi thử nghiệm guard trực tiếp với Azure: candidate thấp hơn bị chặn, ETag model không đổi; cảnh báo phân phối được thử bằng dữ liệu giả 50%, không thay dữ liệu thật.
- `report-bonus.json` và `detail-bonus.txt`: kết quả chạy cục bộ trên train 44.722 mẫu; đã đối chiếu khớp CI run [37642425221](https://github.com/thienphu7/K4-L3-DAY21-LeHoangThienPhu-2A202602908-CI-CD-for-AI-Systems/actions/runs/37642425221). Cả bốn jobs thành công; VM đã load ngưỡng 0.30 và API hoạt động. Log xác minh: `bonus-ci-verification.txt`.
- Kiểm thử cục bộ: 23 tests đạt, gồm API dùng threshold, metrics model đã serialize, per-class report, cả hai nhánh drift và regression guard.
