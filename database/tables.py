from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ProxyInfo(Base):
    __tablename__ = "Proxy_Info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(50), unique=True, nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    status = Column(Enum('active', 'inactive', 'banned'), default='active')
    rotation_time = Column(Integer, nullable=True)

class PhoneInfo(Base):
    __tablename__ = "Phone_Info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    imei = Column(String(50), unique=True, nullable=False)
    device_code = Column(String(50), unique=True, nullable=False)
    adb_device_id = Column(String(50), nullable=True)
    proxy_id = Column(Integer, ForeignKey("Proxy_Info.id"), nullable=True)
    status = Column(Enum('active', 'inactive', 'banned'), default='active')

    proxy = relationship("ProxyInfo", backref="phones")

class TikTokAccount(Base):
    __tablename__ = "TikTok_Account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_id = Column(Integer, ForeignKey("Phone_Info.id"), unique=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)

    phone = relationship("PhoneInfo", backref="tiktok_account")

class PersonalityTag(Base):
    __tablename__ = "Personality_Tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(100), unique=True, nullable=False)

class AccountTag(Base):
    __tablename__ = "Account_Tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tiktok_id = Column(Integer, ForeignKey("TikTok_Account.id"))
    tag_id = Column(Integer, ForeignKey("Personality_Tag.id"))

    tiktok_account = relationship("TikTokAccount", backref="tags")
    personality_tag = relationship("PersonalityTag", backref="accounts")

class TikTokChannel(Base):
    __tablename__ = "TikTok_Channel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("Personality_Tag.id"))
    channel_name = Column(String(255), nullable=False)
    channel_url = Column(String(255), unique=True, nullable=False)

    tag = relationship("PersonalityTag", backref="channels")
