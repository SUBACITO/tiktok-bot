from flask import Flask, request, jsonify
import mysql.connector
from queue import Queue
import threading
import time
import os
import uiautomator2 as u2
import multiprocessing
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

app = Flask(__name__)

# Hàng đợi để gom dữ liệu trước khi ghi vào MySQL
data_queue = Queue()

# Lấy thông tin database từ biến môi trường
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def test_db_connection():
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print("✅ Kết nối MySQL thành công!")
            conn.close()
        else:
            print("❌ Không thể kết nối MySQL.")
    except mysql.connector.Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")


def run_bot(device_id):
    try:
        # Kết nối với thiết bị Android
        d = u2.connect(device_id)
        print(f"Đã kết nối với {device_id}")
        
        d.app_stop_all()

        d.press("back") # press the back key, with key name
        # Mở TikTok
        # d.app_start("com.zhiliaoapp.musically")  # Package name của TikTok
        d(text="TikTok").click()
        # if d(resourceId="com.zhiliaoapp.musically:id/like_button").exists:
        #     d(resourceId="com.zhiliaoapp.musically:id/like_button").click()
        #     print(f"{device_id} đã nhấn like")

        time.sleep(8)
        for i in range(10):  # Change this number to control how many videos to swipe
            print(f"Đang chuyển sang video {i+1}")
            d.swipe_ext("up", scale=1)  # Swipe up to go to the next video
            time.sleep(3)  # Wait before swiping again
        

        
        # # Tương tác với TikTok (Ví dụ: Nhấn nút Like)
        # if d(resourceId="com.zhiliaoapp.musically:id/like_button").exists:
        #     d(resourceId="com.zhiliaoapp.musically:id/like_button").click()
        #     print(f"{device_id} đã nhấn like")
        
        # Đóng ứng dụng sau khi chạy xong
        d.app_stop("com.zhiliaoapp.musically")
    except Exception as e:
        print(f"Lỗi trên thiết bị {device_id}: {e}")



# Hàm kết nối MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# API để gọi bot bằng POST request
@app.route("/run_bot", methods=["POST"])
def run_bot_api():
    data = request.json
    device_id = data.get("device_id")

    if not device_id:
        return jsonify({"error": "Thiếu device_id"}), 400

    # Chạy bot trong một process mới để không chặn API
    p = multiprocessing.Process(target=run_bot, args=(device_id,))
    p.start()

    return jsonify({"message": f"Đã bắt đầu bot trên {device_id}"}), 200

# API nhận dữ liệu từ bot
@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.json
    data_queue.put(data)  # Đẩy dữ liệu vào hàng đợi
    return jsonify({"message": "Queued for update"}), 200

# Worker chạy nền để ghi dữ liệu vào MySQL theo batch
def db_worker():
    while True:
        time.sleep(1)  # Gom dữ liệu mỗi 1 giây để giảm tải MySQL
        batch_data = []
        while not data_queue.empty():
            batch_data.append(data_queue.get())

        if batch_data:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Gom nhiều lệnh UPDATE vào 1 query duy nhất
            for data in batch_data:
                cursor.execute("UPDATE bots SET status=%s WHERE device_id=%s", (data["status"], data["device_id"]))

            conn.commit()
            cursor.close()
            conn.close()

# Chạy worker trong thread riêng
threading.Thread(target=db_worker, daemon=True).start()

if __name__ == "__main__":
    test_db_connection()
    app.run(debug=True, port=5000)