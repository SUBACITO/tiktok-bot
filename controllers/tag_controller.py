from flask import Blueprint, request, jsonify
from models import PersonalityTag
from tiktok_bot_farm.config import db

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/tags', methods=['GET'])
def get_all_tags():
    tags = PersonalityTag.query.all()
    return jsonify([t.to_dict() for t in tags])

@tag_bp.route('/tags', methods=['POST'])
def add_tag():
    data = request.json
    new_tag = PersonalityTag(tag_name=data['tag_name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({"message": "Tag added successfully"}), 201
