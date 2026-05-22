from flask import Blueprint, jsonify
from db.database import FarmingCategory

farming_categories_bp = Blueprint(
    "farming_categories",
    __name__,
    url_prefix="/categories"
)

# Compatibility with your old app.py import:
# from blueprints.farming_categories import category_bp
category_bp = farming_categories_bp


@farming_categories_bp.route("", methods=["GET"], strict_slashes=False)
def get_categories():
    categories = FarmingCategory.query.all()
    data = [
        {"category_id": category.category_id, "name": category.name}
        for category in categories
    ]
    return jsonify(data)
