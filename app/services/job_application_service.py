from email.mime import application

from app.extensions import db
from app.models import JobApplication, JobPosting, SeekerProfile

VALID_STATUSES = {
    "Pending",
    "Reviewed",
    "Accepted",
    "Rejected"
}

def serializeApplication(application):
    job = application.jobPosting
    seeker = application.seekerProfile

    return {
        "id": application.id,
        "seekerId": application.seekerId,
        "jobPostingId": application.jobPostingId,
        "status": application.status,
        "appliedDate": application.appliedDate.isoformat()
        if application.appliedDate else None,
        "cv": application.cv,
        "seeker": {
            "id": seeker.id,
            "userId": seeker.userId,
            "fullName": seeker.fullName,
            "email": seeker.user.email if seeker.user else None,
        } if seeker else None,
        "jobPosting": {
            "id": job.id,
            "jobTitle": job.jobTitle,
            "companyName": job.employer.companyName if job.employer else None,
            "jobLocation": job.jobLocation,
            "jobDescription": job.jobDescription,
            "workMode": job.workMode
        } if job else None
    }

def createApplication(data):
    seekerId = data.get("seekerId")
    jobPostingId = data.get("jobPostingId")

    if not seekerId:
        return {
            "success": False,
            "message": "Seeker ID is required"
        }



    if not jobPostingId:
        return {
            "success": False,
            "message": "Job posting ID is required"
        }

    seeker = SeekerProfile.query.get(seekerId)

    if not seeker:
        return {
            "success": False,
            "message": "Seeker profile not found"
        }

    job = JobPosting.query.get(jobPostingId)

    if not job:
        return {
            "success": False,
            "message": "Job posting not found"
        }

    existingApplication = JobApplication.query.filter_by(
        seekerId=seekerId,
        jobPostingId=jobPostingId
    ).first()

    if existingApplication:
        return {
            "success": False,
            "message": "You have already applied for this job"
        }

    application = JobApplication(
        seekerId=seekerId,
        jobPostingId=jobPostingId,
        cv=data.get("cv"),
        status="Pending"
    )

    db.session.add(application)
    db.session.commit()

    return {
        "success": True,
        "message": "Application submitted successfully",
        "application": serializeApplication(application)
    }

def getApplicationById(applicationId):
    application = JobApplication.query.get(applicationId)

    if not application:
        return {
            "success": False,
            "message": "Application not found"
        }

    return {
        "success": True,
        "application": serializeApplication(application)
    }

def getApplicationsBySeeker(seekerId):
    seeker = SeekerProfile.query.get(seekerId)

    if not seeker:
        return {
            "success": False,
            "message": "Seeker profile not found"
        }

    return {
        "success": True,
        "applications": [
            serializeApplication(application)
            for application in seeker.jobApplications
        ]
    }

def getApplicationsByJob(jobPostingId):
    job = JobPosting.query.get(jobPostingId)

    if not job:
        return {
            "success": False,
            "message": "Job posting not found"
        }

    return {
        "success": True,
        "applications": [
            serializeApplication(application)
            for application in job.jobApplications
        ]
    }

def updateApplicationStatus(applicationId, status):
    application = JobApplication.query.get(applicationId)

    if not application:
        return {
            "success": False,
            "message": "Application not found"
        }

    if status not in VALID_STATUSES:
        return {
            "success": False,
            "message": "Invalid application status"
        }

    application.status = status
    db.session.commit()

    return {
        "success": True,
        "message": "Application status updated successfully",
        "application": serializeApplication(application)
    }

def deleteApplication(applicationId):
    application = JobApplication.query.get(applicationId)

    if not application:
        return {
            "success": False,
            "message": "Application not found"
        }

    db.session.delete(application)
    db.session.commit()

    return {
        "success": True,
        "message": "Application deleted successfully"
    }


