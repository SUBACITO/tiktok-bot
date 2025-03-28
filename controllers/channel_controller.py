from flask import Blueprint, request, jsonify
from models import TikTokChannel
from tiktok_bot_farm.config import db

channel_bp = Blueprint('channel', __name__)

@channel_bp.route('/channels', methods=['GET'])
def get_all_channels():
    channels = TikTokChannel.query.all()
    return jsonify([c.to_dict() for c in channels])

@channel_bp.route('/channels', methods=['POST'])
def add_channel():
    data = request.json
    new_channel = TikTokChannel(channel_name=data['channel_name'], channel_url=data['channel_url'])
    db.session.add(new_channel)
    db.session.commit()
    return jsonify({"message": "Channel added successfully"}), 201
