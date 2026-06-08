# 📚 Hệ Thống Chia Sẻ Tài Liệu
# Thành viên: |1.NGuyễn Văn Tùng Khánh| 2.Dinh Quốc Thái| 3.Nguyễn Tiến Thịnh|
Ứng dụng web chia sẻ tài liệu học tập xây dựng bằng **Flask** + **SQLite**, hỗ trợ đăng ký/đăng nhập, upload, tìm kiếm, sửa và xóa tài liệu.

---

## 📁 Cấu Trúc Dự Án

```
project/
├── main.py                   # File chính: khởi tạo app, định nghĩa routes
├── models.py                 # Định nghĩa các model: User, Document
│
├── app/
│   └── static/
│       └── uploads/          # Thư mục lưu file tải lên (tự tạo khi chạy)
│
├── templates/
│   ├── index.html            # Trang chủ – danh sách tài liệu + tìm kiếm
│   ├── login.html            # Trang đăng nhập
│   ├── register.html         # Trang đăng ký tài khoản
│   ├── upload.html           # Trang tải tài liệu lên
│   └── edit.html             # Trang sửa tên tài liệu
│
├── instance/
│   └── database.db           # File SQLite (tự tạo khi chạy lần đầu)
│
└── README.md
```

---

## ⚙️ Cài Đặt

### Yêu cầu
- Python 3.8+
- pip

### Các bước

**1. Clone hoặc tải về dự án**
```bash
git clone <url-repo>
cd project
```

**2. Tạo môi trường ảo (khuyến nghị)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Cài đặt thư viện**
```bash
pip install flask flask-sqlalchemy flask-login
```

---

## ▶️ Chạy Ứng Dụng

```bash
python main.py
```

Mở trình duyệt và truy cập: **http://127.0.0.1:5000**

> Database `database.db` và thư mục `app/static/uploads/` sẽ được tạo tự động ở lần chạy đầu tiên.

---

## 🧩 Tính Năng

| Tính năng                           | Đường dẫn      | Yêu cầu đăng nhập |
|-------------------------------------|----------------|-------------------|
| Trang chủ – xem & tìm kiếm tài liệu | `/`            | Không             |
| Đăng ký tài khoản                   | `/register`    | Không             |
| Đăng nhập                           | `/login`       | Không             |
| Đăng xuất                           | `/logout`      | Có                |
| Upload tài liệu                     | `/upload`      | Có                |
| Sửa tên tài liệu                    | `/edit/<id>`   | Có                |
| Xóa tài liệu                        | `/delete/<id>` | Có                |

---

## 🗄️ Mô Hình Dữ Liệu

**User** – Tài khoản người dùng
- `id`, `username` (unique), `password`

**Document** – Tài liệu được upload
- `id`, `filename` (tên lưu server), `original_name` (tên gốc), `file_type`, `user_id` (khóa ngoại → User)

---

## 🛠️ Công Nghệ Sử Dụng

- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** Tailwind CSS, Font Awesome
