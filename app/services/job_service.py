from app.models import JobPosting
from app.services import filter_service

def serializeSkill(skill):
    return {
        "id": skill.id,
        "name": skill.name
    }

def serializeJob(job):
    return {
        "id": job.id,
        "jobTitle": job.jobTitle,
        "companyInformation": job.companyInformation,
        "jobDescription": job.jobDescription,
        "requiredEducation": job.requiredEducation,
        "yearsOfExperience": job.yearsOfExperience,
        "workMode": job.workMode,
        "jobLocation": job.jobLocation,
        "skills": [serializeSkill(skill) for skill in job.skills]
    }

def getAllJobs():
    jobs = JobPosting.query.all()

    return {
        "success": True,
        "jobs": [serializeJob(job) for job in jobs]
    }

def getJobById(jobId):
    job = JobPosting.query.get(jobId)

    if not job:
        return {
            "success": False,
            "message": "Job not found"
        }

    return {
        "success": True,
        "job": serializeJob(job)
    }

def searchJobs(filters):
    jobs = JobPosting.query.all()

    filteredJobs = filter_service.filterJobs(
        jobs,
        keywords = filters.get("keywords"),
        location = filters.get("location"),
        workMode = filters.get("workMode"),
        education = filters.get("education"),
        maxExperience = filters.get("maxExperience"),
        skills = filters.get("skills"),
    )

    return {
        "success": True,
        "jobs": [serializeJob(job) for job in filteredJobs]
    }

def parseInt(value):
    if value in (None, ""):
        return None

    try:
        return int(value)
    except ValueError:
        return None
