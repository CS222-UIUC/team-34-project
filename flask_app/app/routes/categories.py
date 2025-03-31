from flask import Blueprint, jsonify
from app.models import Category

categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])
