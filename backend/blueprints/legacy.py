"""Old working URLs kept as aliases.

Use these only to avoid breaking your previous tests. Prefer the cleaner
REST URLs from the section blueprints, for example /direct_payments.
"""

from flask import Blueprint

from blueprints.direct_payment_categories import (
    create_direct_payment_category,
    get_direct_payment_categories,
)
from blueprints.direct_payments import (
    create_direct_payment_observation,
    delete_direct_payment_observation,
    get_direct_payment_observations,
    get_direct_payment_observations_filtered,
)

legacy_bp = Blueprint("legacy", __name__)


@legacy_bp.route("/direct_payment_category", methods=["POST"])
def legacy_create_direct_payment_category():
    return create_direct_payment_category()


@legacy_bp.route("/direct_payment_observation", methods=["POST"])
def legacy_create_direct_payment_observation():
    return create_direct_payment_observation()


@legacy_bp.route("/get_payment_categories", methods=["GET"])
def legacy_get_direct_payment_categories():
    return get_direct_payment_categories()


@legacy_bp.route("/get_payment_observations", methods=["GET"])
def legacy_get_direct_payment_observations():
    return get_direct_payment_observations()


@legacy_bp.route("/get_payment_categories/filter", methods=["GET"])
def legacy_filter_direct_payment_observations():
    # This keeps your old route name, but it actually filters payment observations.
    return get_direct_payment_observations_filtered()


@legacy_bp.route("/del_observations/<int:direct_payment_observation_id>", methods=["DELETE"])
def legacy_delete_direct_payment_observation(direct_payment_observation_id):
    return delete_direct_payment_observation(direct_payment_observation_id)
