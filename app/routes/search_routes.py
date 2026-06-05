from flask import Blueprint, jsonify, request
from app.services import search_service

searchBp = Blueprint("search", __name__, url_prefix="/api/search")

@searchBp.route("/jobs", methods=["GET"])
def searchJobs():
    filters = {
        "keywords": request.args.get("keywords"),
        "location": request.args.get("location"),
        "workMode": request.args.get("workMode"),
        "education": request.args.get("education"),
        "maxExperience": request.args.get("maxExperience"),
        "skills": request.args.get("skills"),
        "fuzzy": request.args.get("fuzzy")
    }
    result = search_service.searchJobs(filters)
    return jsonify(result), 200

@searchBp.route("/candidates", methods=["GET"])
def searchCandidates():
    filters = {
        "keywords": request.args.get("keywords"),
        "location": request.args.get("location"),
        "workMode": request.args.get("workMode"),
        "education": request.args.get("education"),
        "minExperience": request.args.get("minExperience"),
        "skills": request.args.get("skills"),
        "fuzzy": request.args.get("fuzzy")
    }
    result = search_service.searchCandidates(filters)
    return jsonify(result), 200

