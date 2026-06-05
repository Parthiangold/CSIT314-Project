from flask import Blueprint, request, jsonify
from app.services import job_service

jobBp = Blueprint("jobs", __name__, url_prefix="/api/jobs")

@jobBp.route("", methods=["GET"])
def getAllJobs():
    result = job_service.getAllJobs()
    return jsonify(result), 200

@jobBp.route("/<int:jobId>", methods=["GET"])
def getJobById(jobId):
    result = job_service.getJobById(jobId)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@jobBp.route("/search", methods=["GET"])
def searchJobs():
    filters = {
        "keywords": request.args.get("keywords"),
        "location": request.args.get("location"),
        "workMode": request.args.get("workMode"),
        "education": request.args.get("education"),
        "maxExperience": request.args.get("maxExperience"),
        "skills": request.args.getlist("skills"),
    }

    result = job_service.searchJobs(filters)
    return jsonify(result), 200