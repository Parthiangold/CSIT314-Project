from flask import Blueprint, request, jsonify
from app.services import job_application_service

applicationBp = Blueprint("applications", __name__, url_prefix="/api/applications")

@applicationBp.route("", methods=["POST"])
def createApplication():
    data = request.get_json(silent=True) or {}

    result = job_application_service.createApplication(data)
    status = 201 if result['success'] else 400

    if result.get("message") in (
            "Seeker profile not found",
            "Job posting not found"
    ):
        status = 404

    return jsonify(result), status

@applicationBp.route("/<int:applicationId>", methods=["GET"])
def getApplicationById(applicationId):
    result = job_application_service.getApplicationById(applicationId)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@applicationBp.route("/seeker/<int:seekerId>", methods=["GET"])
def getApplicationsBySeeker(seekerId):
    result = job_application_service.getApplicationsBySeeker(seekerId)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@applicationBp.route("/job/<int:jobId>", methods=["GET"])
def getApplicationsByJob(jobId):
    result = job_application_service.getApplicationsByJob(jobId)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@applicationBp.route("/<int:applicationId>/status", methods=["PUT"])
def updateApplicationStatus(applicationId):
    data = request.get_json(silent=True) or {}

    result = job_application_service.updateApplicationStatus(
        applicationId,
        data.get("status")
    )
    status = 200 if result['success'] else 400

    if result.get("message") == "Application not found":
        status = 404

    return jsonify(result), status

@applicationBp.route("/<int:applicationId>", methods=["DELETE"])
def deleteApplication(applicationId):
    result = job_application_service.deleteApplication(applicationId)
    status = 200 if result['success'] else 404

    return jsonify(result), status