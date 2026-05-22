from flask import Blueprint, jsonify, request
from db.database import db, Area

areas_bp = Blueprint("areas", __name__, url_prefix="/areas")


@areas_bp.route("", methods=["GET"], strict_slashes=False)
def get_areas():
    areas = Area.query.all()
    data = [
        {"area_id": area.area_id, "name": area.name}
        for area in areas
    ]
    return jsonify(data)


@areas_bp.route("", methods=["POST"], strict_slashes=False)
def create_area():
    data = request.get_json(silent=True)

    if not data or "name" not in data:
        return jsonify({"error": "Area name required"}), 400

    existing = Area.query.filter_by(name=data["name"]).first()

    if existing:
        return jsonify({"error": "Area already exists"}), 400

    area = Area(name=data["name"])
    db.session.add(area)
    db.session.commit()

    return jsonify({
        "message": "Area created",
        "area": {
            "area_id": area.area_id,
            "name": area.name
        }
    }), 201


@areas_bp.route("/<int:area_id>", methods=["PUT"])
def update_area(area_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    area = db.session.get(Area, area_id)

    if not area:
        return jsonify({"error": "Area not found"}), 404

    if "name" in data:
        area.name = data["name"]

    db.session.commit()

    return jsonify({
        "message": "Area updated",
        "area": {
            "area_id": area.area_id,
            "name": area.name
        }
    })


@areas_bp.route("/<int:area_id>", methods=["DELETE"])
def delete_area(area_id):
    area = db.session.get(Area, area_id)

    if not area:
        return jsonify({"error": "Area not found"}), 404

    area_name = area.name
    db.session.delete(area)
    db.session.commit()

    return jsonify({"message": f"Area '{area_name}' deleted"})
