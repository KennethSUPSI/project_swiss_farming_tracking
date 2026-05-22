from flask import Blueprint, jsonify, request
from db.database import db, DirectPaymentCategory

# This file is plural to match the URL and the variable name.
direct_payment_categories_bp = Blueprint(
    "direct_payment_categories",
    __name__,
    url_prefix="/direct_payment_categories"
)

# Compatibility alias if you accidentally import the singular variable name.
direct_payment_category_bp = direct_payment_categories_bp


@direct_payment_categories_bp.route("", methods=["GET"], strict_slashes=False)
def get_direct_payment_categories():
    categories = DirectPaymentCategory.query.all()

    data = [
        {
            "payment_category_id": category.payment_category_id,
            "name": category.name
        }
        for category in categories
    ]

    return jsonify(data)


@direct_payment_categories_bp.route("", methods=["POST"], strict_slashes=False)
def create_direct_payment_category():
    data = request.get_json(silent=True)

    if not data or "name" not in data:
        return jsonify({"error": "Direct payment category name required"}), 400

    existing = DirectPaymentCategory.query.filter_by(name=data["name"]).first()

    if existing:
        return jsonify({"error": "Direct payment category already exists"}), 400

    category = DirectPaymentCategory(name=data["name"])

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "message": "Direct payment category created",
        "category": {
            "payment_category_id": category.payment_category_id,
            "name": category.name
        }
    }), 201
