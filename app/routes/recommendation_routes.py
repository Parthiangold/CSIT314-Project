from flask import Blueprint, request, jsonify

from app.services import recommendation_service

recommendationBp = Blueprint("recommendations", __name__, url_prefix="/api/recommendations")

@recommendationBp.route("/jobs/seeker/<int:seekerId>", methods=["GET"])
def recommendJobsForSeeker(seekerId):
    result = recommendation_service.recommendJobsForSeeker(seekerId)
    status = 200 if result['success'] else 404

    return jsonify(result), status

@recommendationBp.route("/candidates/job/<int:jobId>", methods=["GET"])
def recommendCandidatesForJob(jobId):
    result = recommendation_service.recommendCandidatesForJob(jobId)
    status = 200 if result['success'] else 404

    return jsonify(result), status