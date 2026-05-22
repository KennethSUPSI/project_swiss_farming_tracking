from flask import Blueprint, jsonify
from db.database import Canton

cantons_bp = Blueprint("cantons", __name__, url_prefix="/cantons")


@cantons_bp.route("", methods=["GET"], strict_slashes=False)
def get_cantons():
    cantons = Canton.query.all()
    data = [
        {"canton_id": canton.canton_id, "name": canton.name}
        for canton in cantons
    ]
    return jsonify(data)
