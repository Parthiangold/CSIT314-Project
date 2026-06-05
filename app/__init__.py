from flask import Flask, render_template
from app.extensions import db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    from app.routes.auth_routes import authBp
    app.register_blueprint(authBp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


createApp = create_app
