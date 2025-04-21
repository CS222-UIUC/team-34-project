from flask import Blueprint, jsonify
from app.models import Category

categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    if not categories:
        return jsonify([])
    return jsonify([category.to_dict() for category in categories])
