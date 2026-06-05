from difflib import SequenceMatcher

from app.models import JobPosting, SeekerProfile, seeker, Skill
from app.services import filter_service, workExperiencesToText

FUZZY_THRESHOLD = 0.72

def serializeSkill(skill):
    return {
        "id": skill.id,
        "name": skill.name
    }

def serializeJob(job):
    return {
        "id": job.employerId,
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

def serializeSeeker(seeker):
    return {
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

def searchJobs(filters):
    jobs = JobPosting.query.all()

    filteredJobs = filter_service.filterJobs(
        jobs,
        keywords=filters.get("keywords"),
        location=filters.get("location"),
        workMode=filters.get("workMode"),
        education=filters.get("education"),
        maxExperience=filters.get("maxExperience"),
        skills=filters.get("skills"),
    )

    if shouldUseFuzzySearch(filters):
        filteredJobs = applyFuzzyJobSearch(filteredJobs, filters.get("keywords"))

    return {
        "success": True,
        "jobs": [serializeJob(job) for job in filteredJobs]
    }

def searchCandidates(filters):
    seekers = SeekerProfile.query.all()

    filteredSeekers = filter_service.filterSeekers(
        seekers,
        keywords=filters.get("keywords"),
        location=filters.get("location"),
        workMode=filters.get("workMode"),
        education=filters.get("education"),
        skills=filters.get("skills"),
        minExperience=filters.get("minExperience"),
    )

    if shouldUseFuzzySearch(filters):
        filteredSeekers = applyFuzzyCandidateSearch(
            filteredSeekers,
            filters.get("keywords")
        )

    return {
        "success": True,
        "candidates": [
            serializeSeeker(seeker)
            for seeker in filteredSeekers
        ]
    }

def applyFuzzyJobSearch(jobs, keywords):
    terms = normalizeTerms(keywords)

    if not terms:
        return jobs

    matchedJobs = []

    for job in jobs:
        searchableText = "".join([
            valueToText(job.jobTitle),
            valueToText(job.companyInformation),
            valueToText(job.jobDescription),
            valueToText(job.requiredEducation),
            valueToText(job.workMode),
            valueToText(job.jobLocation),
            skillsToText(job.skills)
        ])

        if fuzzyMatchesAnyTerm(terms, searchableText):
            matchedJobs.append(job)

    return matchedJobs

def applyFuzzyCandidateSearch(seekers, keywords):
    terms = normalizeTerms(keywords)

    if not terms:
        return seekers

    matchedSeekers = []

    for seeker in seekers:
        searchableText = "".join([
            valueToText(seeker.fullName),
            valueToText(seeker.education),
            valueToText(seeker.major),
            valueToText(seeker.fieldOfStudy),
            valueToText(seeker.preferredWorkMode),
            valueToText(seeker.preferredLocation),
            skillsToText(seeker.skills),
            workExperiencesToText(seeker.workExperiences)
        ])

        if fuzzyMatchesAnyTerm(terms, searchableText):
            matchedSeekers.append(seeker)

    return matchedSeekers

def fuzzyMatchesAnyTerm(terms, searchableText):
    words = normalizeText(searchableText).split()

    for term in terms:
        normalizedTerm = normalizeText(term)

        if normalizedTerm in normalizeText(searchableText):
            return True

        for word in words:
            if similarity(normalizedTerm, word) >= FUZZY_THRESHOLD:
                return True

    return False

def shouldUseFuzzySearch(filters):
    value = filters.get("fuzzy")

    if value is None:
        return False

    return str(value).strip().lower() in (1, "true", "yes")

def similarity(firstValue, secondValue):
    return SequenceMatcher(
        None,
        firstValue,
        secondValue
    ).ratio()

def ParseInt(value):
    if value in (None, ""):
        return None

    try:
        return int(value)
    except ValueError:
        return None

def normalizeTerms(value):
    if value is None:
        return []

    if isinstance(value, str):
        value = value.split(",")

    terms = []

    for item in value:
        term = str(item).strip()

        if term:
            terms.append(term)

    return terms

def normalizeText(value):
    return str(value).strip().lower()

def valueToText(value):
    if value is None:
        return ""

    return str(value)

def skillsToText(skills):
    return "".join(
        skill.name
        for skill in skills
    )

def workExperiencesToText(workExperiences):
    return "".join(
        f"{workExperience.workPlaceName} {workExperience.role}"
        for workExperience in workExperiences
    )