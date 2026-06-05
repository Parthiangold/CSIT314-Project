from flask import Blueprint, request, jsonify

from app.services import employer_service

employerBp = Blueprint("employers", __name__, url_prefix="/api/employers")

@employerBp.route("", methods=["GET"])
def getAllEmployers():
    result = employer_service.getAllEmployers()
    return jsonify(result), 200


@employerBp.route("/<int:employerId>", methods=["GET"])
def getEmployerById(employerId):
    result = employer_service.getEmployerById(employerId)
    status = 200 if result['success'] else 404
    return jsonify(result), status

@employerBp.route("/user/<int:userId>", methods=["GET"])
def getEmployerByUserId(userId):
    result = employer_service.getEmployerByUserId(userId)
    status = 200 if result['success'] else 404
    return jsonify(result), status

@employerBp.route("/user/<int:userId>", methods=["PUT"])
def saveEmployerProfile(userId):
    data = request.get_json(silent=True) or {}
    result = employer_service.saveEmployerProfile(userId, data)
    status = 200 if result['success'] else 400

    if result.get("message") == "User not found":
        status = 404

    return jsonify(result), status

@employerBp.route("/user/<int:userId>/jobs", methods=["GET"])
def getEmployerJobPostings(userId):
    result = employer_service.getEmployerJobPostings(userId)
    status = 200 if result['success'] else 404
    return jsonify(result), status

@employerBp.route("/user/<int:userId>/jobs", methods=["POST"])
def createJobPosting(userId):
    data = request.get_json(silent=True) or {}

    result = employer_service.createJobPosting(userId, data)
    status = 201 if result['success'] else 400

    if result.get("message") == "Employer profile not found":
        status = 404

    return jsonify(result), status

@employerBp.route("/jobs/<int:jobId>", methods=["PUT"])
def updateJobPosting(jobId):
    data = request.get_json(silent=True) or {}

    result = employer_service.updateJobPosting(jobId, data)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@employerBp.route("/jobs/<int:jobId>", methods=["DELETE"])
def deleteJobPosting(jobId):
    result = employer_service.deleteJobPosting(jobId)
    status = 200 if result['success'] else 404

    return jsonify(result), status