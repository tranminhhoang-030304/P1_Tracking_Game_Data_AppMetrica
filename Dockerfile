# 1. Dùng Python 3.9 bản nhẹ
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# 2. Thiết lập thư mục làm việc trong container
WORKDIR /app

# 4. Copy file thư viện và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ code dự án vào container
COPY . .

# 6. Mở cổng 8000 (để Web chạy)
EXPOSE 8000

# 7. Lệnh mặc định: Chạy cả Web Server và Scheduler cùng lúc (dùng script)
# Tuy nhiên để đơn giản cho Docker Compose, ta sẽ set lệnh chạy Web làm mặc định
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]