from flask import Blueprint, request, jsonify
from models import Proxy
from tiktok_bot_farm.config import db  # Import model Proxy

proxy_bp = Blueprint('proxy', __name__)

@proxy_bp.route('/proxies', methods=['GET'])
def get_all_proxies():
    proxies = Proxy.query.all()
    return jsonify([p.to_dict() for p in proxies])

@proxy_bp.route('/proxies', methods=['POST'])
def add_proxy():
    data = request.json
    new_proxy = Proxy(ip_address=data['ip_address'], port=data['port'])
    db.session.add(new_proxy)
    db.session.commit()
    return jsonify({"message": "Proxy added successfully"}), 201
