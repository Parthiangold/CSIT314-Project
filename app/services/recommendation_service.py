from app.models import JobPosting, SeekerProfile
from app.services import normalizeText

NON_MEMBER_LIMIT = 10

def serializeSkill(skill):
    return {
        "id": skill.id,
        "name": skill.name
    }

def serializeJobRecommendation(job, score):
    return {
        "score": score,
        "job": {
            "id": job.id,
            "employerId": job.employerid,
            "companyName": job.employer.companyName if job.employer else None,
            "jobTitle": job.jobTitle,
            "companyInformation": job.companyInformation,
            "jobDescription": job.jobDescription,
            "requiredEducation": job.requiredEducation,
            "yearsOfExperience": job.yearsOfExperience,
            "workMode": job.workMode,
            "jobLocation": job.jobLocation,
            "skills": [serializeSkill(skill) for skill in job.skills]
        }
    }

def serializeCandidateRecommendation(seeker, score):
    return {
        "score": score,
        "candidate": {
            "id": seeker.id,
            "userId": seeker.userId,
            "fullName": seeker.fullName,
            "email": seeker.user.email if seeker.user else None,
            "contact": seeker.pNumber if seeker.user else None,
            "education": seeker.education,
            "major": seeker.major,
            "fieldOfStudy": seeker.fieldOfStudy,
            "yearsOfExperience": seeker.yearsOfExperience,
            "preferredWorkMode": seeker.preferredWorkMode,
            "preferredLocation": seeker.preferredLocation,
            "skills": [serializeSkill(skill) for skill in seeker.skills]
        }
    }

def recommendJobsForSeeker(seekerId):
    seeker = SeekerProfile.query.get(seekerId)

    if not seeker:
        return {
            "success": False,
            "message": "Seeker not found"
        }

    jobs = JobPosting.query.all()
    scoredJobs = []

    for job in jobs:
        score = scoreJobForSeeker(job, seeker)

        if score > 0:
            scoredJobs.append((job, score))

    scoredJobs.sort(key=lambda item: item[1], reverse=True)
    scoredJobs = applyMembershipLimit(scoredJobs, seeker.user)

    return {
        "success": True,
        "isMember": seeker.user.isMember if seeker.user else False,
        "recommendations": [
            serializeJobRecommendation(job, score)
            for job, score in scoredJobs
        ]
    }

def recommendCandidatesForJob(jobId):
    job = JobPosting.query.get(jobId)

    if not job:
        return {
            "success": False,
            "message": "Job not found"
        }

    seekers = SeekerProfile.query.all()
    scoredSeekers = []

    for seeker in seekers:
        score = scoreCandidateForJob(seeker, job)

        if score > 0:
            scoredSeekers.append((seeker, score))

    scoredSeekers.sort(key=lambda item: item[1], reverse=True)

    employerUser = job.employer.user if job.employer else None
    scoredSeekers = applyMembershipLimit(scoredSeekers, employerUser)

    return {
        "success": True,
        "isMember": employerUser.isMember if employerUser else False,
        "recommendations": [
            serializeCandidateRecommendation(seeker, score)
            for seeker, score in scoredSeekers
        ]
    }

def scoreJobForSeeker(job, seeker):
    score = 0

    score += scoreSkillMatch(seeker.skills, job.skills, 40)
    score += scoreTextMatch(seeker.education, job.requiredEducation, 15)
    score += scoreTextMatch(seeker.preferredWorkMode, job.workMode, 15)
    score += scoreTextMatch(seeker.preferredLocation, job.jobLocation, 10)
    score += scoreExperienceForJob(
        seeker.yearsOfExperience,
        job.yearsOfExperience,
        20
    )

    return score

def scoreCandidateForJob(seeker, job):
    score = 0

    score += scoreSkillMatch(seeker.skills, job.skills, 40)
    score += scoreTextMatch(seeker.education, job.requiredEducation, 15)
    score += scoreTextMatch(seeker.preferredWorkMode, job.workMode, 15)
    score += scoreTextMatch(seeker.preferredLocation, job.jobLocation, 10)
    score += scoreExperienceForJob(
        seeker.yearsOfExperience,
        job.yearsOfExperience,
        20
    )

    return score

def scoreSkillMatch(candidateSkills, jobSkills, maxScore):
    candidateSkillNames = {
        normalizeText(skill.name)
        for skill in candidateSkills
    }
    jobSkillNames = {
        normalizeText(skill.name)
        for skill in jobSkills
    }

    if not candidateSkillNames or not jobSkillNames:
        return 0

    matchedSkills = candidateSkillNames.intersection(jobSkillNames)


    return round(
        maxScore * (len(matchedSkills) / len(jobSkillNames)),
        2
    )

def scoreTextMatch(candidateValue, jobValue, maxScore):
    if not candidateValue or not jobValue:
        return 0

    candidateText = normalizeText(candidateValue)
    jobText = normalizeText(jobValue)

    if candidateText == jobText:
        return maxScore

    if candidateText in jobText or jobText in candidateText:
        return round(maxScore * 0.6, 2)

    return 0

def scoreExperienceForJob(candidateExperience, requiredExperience, maxScore):
    if candidateExperience is None or requiredExperience is None:
        return 0

    if candidateExperience >= requiredExperience:
        return maxScore

    if requiredExperience == 0:
        return maxScore

    return round(
        maxScore * (candidateExperience / requiredExperience),
        2
    )

def applyMembershipLimit(scoredItems, user):
    if user and user.isMember:
        return scoredItems

    return scoredItems[:NON_MEMBER_LIMIT]

def normalizeText(value):
    return str(value).strip().lower()
