from sqlalchemy.orm import Session
from tables import ProxyInfo, PhoneInfo, TikTokAccount, PersonalityTag, AccountTag, TikTokChannel

def get_all_tiktok_accounts(db: Session):
    return db.query(TikTokAccount).all()

def add_tiktok_account(db: Session, username, password, phone_number, phone_id):
    new_account = TikTokAccount(username=username, password=password, phone_number=phone_number, phone_id=phone_id)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def assign_tag_to_account(db: Session, tiktok_id, tag_id):
    new_tag = AccountTag(tiktok_id=tiktok_id, tag_id=tag_id)
    db.add(new_tag)
    db.commit()
