from flask import Blueprint, request, jsonify
from app.services import seeker_service

seekerBp = Blueprint("seekers", __name__, url_prefix="/api/seekers")

@seekerBp.route("", methods=["GET"])
def getAllSeekers():
    result = seeker_service.getAllSeekers()
    return jsonify(result), 200

@seekerBp.route("/<int:seekerId>", methods=["GET"])
def getSeekerById(seekerId):
    result = seeker_service.getSeekerById(seekerId)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@seekerBp.route("/user/<int:userId>", methods=["GET"])
def getSeekerByUserId(userId):
    result = seeker_service.getSeekerByUserId(userId)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@seekerBp.route("/user/<int:userId>", methods=["PUT"])
def saveSeekerProfile(userId):
    data = request.get_json(silent=True) or {}
    result = seeker_service.saveSeekerProfile(userId, data)
    status = 200 if result['success'] else 400

    if result.get("message") == "User not found":
        status = 404

    return jsonify(result), status