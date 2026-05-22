from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
backend_root = str(BACKEND_ROOT)
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from flask import Flask
from db.database import db

from blueprints.areas import areas_bp
from blueprints.cantons import cantons_bp
from blueprints.farming_categories import farming_categories_bp
from blueprints.observations import observations_bp
from blueprints.direct_payment_categories import direct_payment_categories_bp
from blueprints.direct_payments import direct_payments_bp
from blueprints.legacy import legacy_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.json.ensure_ascii = False

    base_dir = Path(__file__).resolve().parent.parent
    db_file = base_dir / "db" / "data.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file.as_posix()}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_blueprints(app)
    register_main_routes(app)

    return app


def register_blueprints(app):
    """Register API sections."""
    app.register_blueprint(areas_bp)
    app.register_blueprint(cantons_bp)
    app.register_blueprint(farming_categories_bp)
    app.register_blueprint(observations_bp)
    app.register_blueprint(direct_payment_categories_bp)
    app.register_blueprint(direct_payments_bp)

    app.register_blueprint(legacy_bp)


def register_main_routes(app):
    @app.route("/")
    def check():
        return "Flask is working"

    @app.route("/routes")
    def list_routes():
        routes = []

        for rule in app.url_map.iter_rules():
            routes.append({
                "url": str(rule),
                "endpoint": rule.endpoint,
                "methods": sorted([
                    method for method in rule.methods
                    if method not in ["HEAD", "OPTIONS"]
                ])
            })

        return sorted(routes, key=lambda route: route["url"])


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
