from flask import Blueprint, request, jsonify
from models import Phone
from tiktok_bot_farm.config import db

phone_bp = Blueprint('phone', __name__)

@phone_bp.route('/phones', methods=['GET'])
def get_all_phones():
    phones = Phone.query.all()
    return jsonify([p.to_dict() for p in phones])

@phone_bp.route('/phones', methods=['POST'])
def add_phone():
    data = request.json
    new_phone = Phone(imei=data['imei'], device_code=data['device_code'])
    db.session.add(new_phone)
    db.session.commit()
    return jsonify({"message": "Phone added successfully"}), 201
