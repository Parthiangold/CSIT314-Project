from flask import Blueprint, jsonify, request

from app.services import user_service

userBp = Blueprint("users", __name__, url_prefix="/api/users")


@userBp.route("", methods=["GET"])
def getAllUsers():
    result = user_service.getAllUsers()
    return jsonify(result), 200

@userBp.route("/<int:userId>", methods=["GET"])
def getuserById(userId):
    result = user_service.getUserById(userId)
    status = 200 if result['success'] else 404
    return jsonify(result), status

@userBp.route("/<int:userId>", methods=["PUT"])
def updateUser(userId):
    data = request.get_json(silent=True) or {}
    result = user_service.updateUser(userId, data)

    status = 200 if result['success'] else 400
    return jsonify(result), status

@userBp.route("/<int:userId>/membership", methods=["PUT"])
def updateMembership(userId):
    data = request.get_json(silent=True) or {}

    result = user_service.updateMembership(
        userId,
        data.get("isMember")
    )
    status = 200 if result['success'] else 404

    return jsonify(result), status

@userBp.route("/<int:userId>", methods=["DELETE"])
def deleteUser(userId):
    result = user_service.deleteUser(userId)
    status = 200 if result['success'] else 404

    return jsonify(result), status


