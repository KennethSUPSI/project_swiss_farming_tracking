from flask import Blueprint, jsonify, request
from db.database import db, Observation

observations_bp = Blueprint("observations", __name__, url_prefix="/observations")


def observation_to_dict(observation):
    return {
        "observation_id": observation.observation_id,
        "area": observation.area.name if observation.area else None,
        "canton": observation.canton.name if observation.canton else None,
        "category": observation.category.name if observation.category else None,
        "value": observation.value
    }


@observations_bp.route("", methods=["GET"], strict_slashes=False)
def get_observations():
    observations = Observation.query.all()
    return jsonify([
        observation_to_dict(observation)
        for observation in observations
    ])


@observations_bp.route("/filter", methods=["GET"])
def get_observations_filtered():
    area_id = request.args.get("area_id", type=int)
    canton_id = request.args.get("canton_id", type=int)
    category_id = request.args.get("category_id", type=int)
    min_value = request.args.get("min_value", type=float)
    max_value = request.args.get("max_value", type=float)

    query = Observation.query

    if area_id:
        query = query.filter(Observation.area_id == area_id)
    if canton_id:
        query = query.filter(Observation.canton_id == canton_id)
    if category_id:
        query = query.filter(Observation.category_id == category_id)
    if min_value is not None:
        query = query.filter(Observation.value >= min_value)
    if max_value is not None:
        query = query.filter(Observation.value <= max_value)

    observations = query.all()

    return jsonify([
        observation_to_dict(observation)
        for observation in observations
    ])


@observations_bp.route("", methods=["POST"], strict_slashes=False)
def create_observation():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required_fields = ["area_id", "canton_id", "category_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        observation = Observation(
            area_id=data["area_id"],
            canton_id=data["canton_id"],
            category_id=data["category_id"],
            value=data.get("value")
        )

        db.session.add(observation)
        db.session.commit()

        return jsonify({
            "message": "Observation created",
            "observation_id": observation.observation_id
        }), 201

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@observations_bp.route("/<int:observation_id>", methods=["GET"])
def get_observation(observation_id):
    observation = db.session.get(Observation, observation_id)

    if not observation:
        return jsonify({"error": "Observation not found"}), 404

    return jsonify(observation_to_dict(observation))


@observations_bp.route("/<int:observation_id>", methods=["DELETE"])
def delete_observation(observation_id):
    observation = db.session.get(Observation, observation_id)

    if not observation:
        return jsonify({"error": "Observation not found"}), 404

    db.session.delete(observation)
    db.session.commit()

    return jsonify({"message": f"Observation {observation_id} deleted"})
