from flask import Blueprint, request, jsonify
from models import TikTokAccount
from tiktok_bot_farm.config import db

account_bp = Blueprint('account', __name__)

@account_bp.route('/accounts', methods=['GET'])
def get_all_accounts():
    accounts = TikTokAccount.query.all()
    return jsonify([a.to_dict() for a in accounts])

@account_bp.route('/accounts', methods=['POST'])
def add_account():
    data = request.json
    new_account = TikTokAccount(username=data['username'], password=data['password'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"message": "Account added successfully"}), 201
