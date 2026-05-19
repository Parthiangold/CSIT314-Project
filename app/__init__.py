from flask import Flask
from app.extensions import db, argon

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)
    argon.init_app(app)

    return app