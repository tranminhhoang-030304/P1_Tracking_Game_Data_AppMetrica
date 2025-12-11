# 🚀 Game Data Center - Hệ Thống Phân Tích & ETL Dữ Liệu Game

> **Hệ thống tự động hóa quy trình ETL (Extract - Transform - Load) từ Oracle về Data Warehouse, cung cấp Dashboard theo dõi doanh thu và hành vi người chơi theo thời gian thực.**

---

## 📖 Giới thiệu
Dự án được xây dựng để giải quyết bài toán theo dõi chỉ số game (Game Analytics) một cách tự động. Hệ thống sử dụng kiến trúc **Hybrid (Lai ghép)** thông minh để vượt qua rào cản mạng doanh nghiệp, kết nối trực tiếp với Oracle Server để lấy dữ liệu.

### ✨ Tính năng nổi bật
* **📊 Real-time Dashboard:** Biểu đồ doanh thu, tỷ lệ thắng/thua (Fail Rate) và phân tích hành vi sử dụng vật phẩm (Drill-down Analytics).
* **🔄 Smart ETL Scheduler:** Tự động đồng bộ dữ liệu theo chu kỳ cấu hình (5 phút, 30 phút...) mà không cần khởi động lại.
* **🛠️ Full Admin CRUD:** Quản lý thêm/sửa/xóa vật phẩm (Booster), chỉnh sửa giá tiền và cấu hình hệ thống ngay trên Web.
* **🕵️ Job Monitoring:** Giám sát trạng thái chạy (Success/Fail), xem log chi tiết, cảnh báo lỗi kết nối.
* **⚡ Hybrid Deployment:** Database chạy trên Docker (ổn định) + Worker chạy trên Windows (tốc độ cao, không bị chặn mạng).

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

### Backend & Core
* **Python 3.10**: Ngôn ngữ xử lý chính.
* **FastAPI**: Xây dựng Web Admin & RESTful API.
* **SQLAlchemy**: ORM tương tác với Database.
* **Pandas**: Xử lý, làm sạch và tổng hợp dữ liệu (Dataframe).
* **Schedule**: Bộ lập lịch chạy tác vụ ngầm.

### Database & Infrastructure
* **PostgreSQL 15**: Data Warehouse lưu trữ dữ liệu (Chạy trên Docker).
* **Docker & Docker Compose**: Đóng gói môi trường Database.
* **OracleDB**: Driver kết nối dữ liệu nguồn.

### Frontend
* **HTML5 / Bootstrap 5**: Giao diện quản trị hiện đại.
* **Chart.js**: Vẽ biểu đồ tương tác (Bar, Line, Doughnut).

---

## ⚙️ Hướng dẫn Cài đặt & Vận hành

### 1. Chuẩn bị môi trường
* Cài đặt **Docker Desktop** và **Python 3.10+**.
* Clone dự án về máy:
  ```bash
  git clone [https://github.com/tranminhhoang-030304/P1_Tracking_Game_Data_AppMetrica.git](https://github.com/tranminhhoang-030304/P1_Tracking_Game_Data_AppMetrica.git)
  cd P1_Tracking_Game_Data_AppMetrica