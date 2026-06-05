from app.extensions import db
from app.models import EmployerProfile, JobPosting, Skill, User

def SerializeSkill(skill):
    return {
        "id": skill.id,
        "name": skill.name
    }

def serializeJobPosting(job):
    return {
        "id": job.id,
        "employerId": job.employer.id,
        "jobTitle": job.jobTitle,
        "companyInformation": job.companyInformation,
        "jobDescription": job.jobDescription,
        "requiredEducation": job.requiredEducation,
        "yearsOfExperience": job.yearsOfExperience,
        "workMode": job.workMode,
        "jobLocation": job.jobLocation,
        "skills": [SerializeSkill(skill) for skill in job.skills],
    }

def serializeEmployerProfile(employerProfile):
    return {
        "id": employerProfile.id,
        "userId": employerProfile.userId,
        "companyName": employerProfile.companyName,
        "contact": employerProfile.pNumber if employerProfile.user else None,
        "email": employerProfile.user.email if employerProfile.user else None,
        "jobPostings": [
            serializeJobPosting(job)
            for job in employerProfile.jobPostings
        ]
    }

def getAllEmployers():
    employers = EmployerProfile.query.all()
    return {
        "success": True,
        "employers": [
            serializeEmployerProfile(employer)
            for employer in employers
        ]
    }

def getEmployerById(employerId):
    employer = EmployerProfile.query.get(employerId)

    if not employer:
        return {
            "success": False,
            "message": "Employer profile not found"
        }

    return {
        "success": True,
        "employer": serializeEmployerProfile(employer)
    }

def getEmployerByUserId(userId):
    employer = EmployerProfile.query.filter_by(userId=userId).first()

    if not employer:
        return {
            "success": False,
            "message": "Employer profile not found"
        }

    return {
        "success": True,
        "employer": serializeEmployerProfile(employer)
    }

def saveEmployerProfile(userId, data):
    user = User.query.get(userId)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if user.userType != "employer":
        return {
            "success": False,
            "message": "User is not an employer"
        }

    employer = EmployerProfile.query.filter_by(userId=userId).first()

    if not employer:
        employer = EmployerProfile(
            userId=userId,
            companyName=data.get("companyName") or user.userName
        )
        db.session.add(employer)

    employer.companyName = data.get("companyName", employer.companyName)
    employer.companyInformation = data.get("companyInformation", employer.companyInformation)
    employer.location = data.get("location", employer.location)

    if "contact" in data:
        user.pNumber = data.get("contact")

    db.session.commit()

    return {
        "success": True,
        "message": "Employer profile saved successfully",
        "employer": serializeEmployerProfile(employer)
    }

def createJobPosting(userId, data):
    employer = EmployerProfile.query.filter_by(userId=userId).first()

    if not employer:
        return {
            "success": False,
            "message": "Employer profile not found"
        }

    if not data.get("jobTitle"):
        return {
            "success": False,
            "message": "Job title is required"
        }

    if not data.get("jobDescription"):
        return {
            "success": False,
            "message": "Job description is required"
        }

    job = JobPosting(
        employerId=employer.id,
        jobTitle=data.get("jobTitle"),
        companyInformation=data.get("companyInformation", employer.companyInformation),
        jobDescription=data.get("jobDescription"),
        requiredEducation=data.get("requiredEducation"),
        yearsOfExperience=data.get("yearsOfExperience"),
        workMode=data.get("workMode"),
        jobLocation=data.get("jobLocation")
    )

    job.skills = buildSkillList(data.get("skills"))

    db.session.add(job)
    db.session.commit()

    return {
        "success": True,
        "message": "Job posting created successfully",
        "job": serializeJobPosting(job)
    }

def updateJobPosting(jobId, data):
    job = JobPosting.query.get(jobId)

    if not job:
        return {
            "success": False,
            "message": "Job posting not found"
        }

    job.jobTitle = data.get("jobTitle", job.jobTitle)
    job.companyInformation = data.get("CompanyInformation", job.companyInformation)
    job.jobDescription = data.get("jobDescription", job.jobDescription)
    job.requiredEducation = data.get("requiredEducation", job.requiredEducation)
    job.yearsOfExperience = data.get("yearsOfExperience", job.yearsOfExperience)
    job.workMode = data.get("workMode", job.workMode)
    job.jobLocation = data.get("jobLocation", job.jobLocation)

    if "skills" in data:
        job.skills = buildSkillList(data.get("skills"))

    db.session.commit()

    return {
        "success": True,
        "message": "Job posting updated successfully",
        "job": serializeJobPosting(job)
    }

def deleteJobPosting(jobId):
    job = JobPosting.query.get(jobId)

    if not job:
        return {
            "success": False,
            "message": "Job posting not found"
        }

    db.session.delete(job)
    db.session.commit()

    return {
        "success": True,
        "message": "Job posting deleted successfully"
    }

def getEmployerJobPostings(userId):
    employer = EmployerProfile.query.filter_by(userId=userId).first()

    if not employer:
        return {
            "success": False,
            "message": "Employer profile not found"
        }

    return {
        "success": True,
        "jobPostings": [
            serializeJobPosting(job)
            for job in employer.jobPostings
        ]
    }

def buildSkillList(rawSkills):
    skillNames = normalizeSkillNames(rawSkills)
    skills = []

    for skillName in skillNames:
        skill = Skill.query.filter_by(name=skillName).first()

        if not skill:
            skill = Skill(name=skillName)
            db.session.add(skill)

        skills.append(skill)

    return skills

def normalizeSkillNames(rawSkills):
    if rawSkills is None:
        return []

    if isinstance(rawSkills, str):
        rawSkills = rawSkills.split(",")

    skillNames = []

    for skill in rawSkills:
        if isinstance(skill, dict):
            skill = skill.get("name")

        if not skill:
            continue

        skillName = str(skill).strip()

        if skillName and skillName not in skillNames:
            skillNames.append(skillName)

    return skillNames

