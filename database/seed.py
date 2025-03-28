from sqlalchemy.orm import sessionmaker
from init_db import engine
from tables import ProxyInfo, PhoneInfo, TikTokAccount, PersonalityTag, TikTokChannel

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def seed_data():
    # Thêm Proxy
    proxy = ProxyInfo(ip_address="123.456.78.9", port=8080, username="user", password="pass", status="active")
    db.add(proxy)
    db.commit()

    # Thêm Phone
    phone = PhoneInfo(imei="1234567890", device_code="Device001", adb_device_id="ADB123", proxy_id=proxy.id, status="active")
    db.add(phone)
    db.commit()

    # Thêm Tài khoản TikTok
    account = TikTokAccount(username="test_user", password="123456", phone_number="0123456789", phone_id=phone.id)
    db.add(account)
    db.commit()

    # Thêm Tag tính cách
    tag1 = PersonalityTag(tag_name="Học tiếng Nhật")
    tag2 = PersonalityTag(tag_name="Văn hóa Nhật")
    db.add(tag1)
    db.add(tag2)
    db.commit()

    # Thêm Kênh TikTok liên quan
    channel = TikTokChannel(tag_id=tag1.id, channel_name="Learn Japanese", channel_url="https://tiktok.com/@japaneselearning")
    db.add(channel)
    db.commit()

    print("Dữ liệu mẫu đã được thêm vào!")

if __name__ == "__main__":
    seed_data()
