from flask import Blueprint, jsonify, request
from db.database import db, DirectPaymentObservation

direct_payments_bp = Blueprint(
    "direct_payments",
    __name__,
    url_prefix="/direct_payments"
)


def direct_payment_observation_to_dict(observation):
    return {
        "direct_payment_observation_id": observation.direct_payment_observation_id,
        "canton": observation.canton.name if observation.canton else None,
        "payment_category": (
            observation.payment_category.name
            if observation.payment_category
            else None
        ),
        "value": observation.value
    }


@direct_payments_bp.route("", methods=["GET"], strict_slashes=False)
def get_direct_payment_observations():
    observations = DirectPaymentObservation.query.all()

    return jsonify([
        direct_payment_observation_to_dict(observation)
        for observation in observations
    ])


@direct_payments_bp.route("/filter", methods=["GET"])
def get_direct_payment_observations_filtered():
    canton_id = request.args.get("canton_id", type=int)
    payment_category_id = request.args.get("payment_category_id", type=int)
    min_value = request.args.get("min_value", type=float)
    max_value = request.args.get("max_value", type=float)

    query = DirectPaymentObservation.query

    if canton_id:
        query = query.filter(DirectPaymentObservation.canton_id == canton_id)

    if payment_category_id:
        query = query.filter(
            DirectPaymentObservation.payment_category_id == payment_category_id
        )

    if min_value is not None:
        query = query.filter(DirectPaymentObservation.value >= min_value)

    if max_value is not None:
        query = query.filter(DirectPaymentObservation.value <= max_value)

    observations = query.all()

    return jsonify([
        direct_payment_observation_to_dict(observation)
        for observation in observations
    ])


@direct_payments_bp.route("", methods=["POST"], strict_slashes=False)
def create_direct_payment_observation():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required_fields = ["canton_id", "payment_category_id", "value"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        observation = DirectPaymentObservation(
            canton_id=data["canton_id"],
            payment_category_id=data["payment_category_id"],
            value=data.get("value")
        )

        db.session.add(observation)
        db.session.commit()

        return jsonify({
            "message": "Direct payment observation created",
            "direct_payment_observation_id": observation.direct_payment_observation_id
        }), 201

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@direct_payments_bp.route("/<int:direct_payment_observation_id>", methods=["GET"])
def get_direct_payment_observation(direct_payment_observation_id):
    observation = db.session.get(
        DirectPaymentObservation,
        direct_payment_observation_id
    )

    if not observation:
        return jsonify({"error": "Direct payment observation not found"}), 404

    return jsonify(direct_payment_observation_to_dict(observation))


@direct_payments_bp.route("/<int:direct_payment_observation_id>", methods=["DELETE"])
def delete_direct_payment_observation(direct_payment_observation_id):
    observation = db.session.get(
        DirectPaymentObservation,
        direct_payment_observation_id
    )

    if not observation:
        return jsonify({"error": "Direct payment observation not found"}), 404

    db.session.delete(observation)
    db.session.commit()

    return jsonify({
        "message": (
            f"Direct payment observation "
            f"{direct_payment_observation_id} deleted"
        )
    })
