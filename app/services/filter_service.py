from app.models import WorkExperience


def filterJobs(
        jobs,
        keywords = None,
        location = None,
        workMode = None,
        education = None,
        maxExperience = None,
        skills = None,
):
    filteredJobs = []

    for job in jobs:
        if keywords and not matchesKeywords(
            keywords,
            [
                job.title,
                job.companyInformation,
                job.description,
                job.requiredEducation,
                job.jobLocation,
                job.workMode,
                skillsToText(job.skills)
            ]
        ):
            continue

        if location and not containsText(job.jobLocation, location):
            continue

        if workMode and not equalsText(job.workMode, workMode):
            continue

        if education and not containsText(job.requiredEducation, education):
            continue

        if maxExperience is not None:
            if job.yearsOfExperience is None:
                continue

            if job.yearsOfExperience > maxExperience:
                continue

        if skills and not matchesAnySkill(job.skills, skills):
            continue

        filteredJobs.append(job)

    return filteredJobs

def filterSeekers(
        seekers,
        keywords = None,
        location = None,
        education = None,
        skills = None,
        workMode = None,
        minExperience = None,
):
    filteredSeekers = []

    for seeker in seekers:
        if keywords and not matchesKeywords(
            keywords,
            [
                seeker.fullName,
                seeker.education,
                seeker.major,
                seeker.fieldOfStudy,
                seeker.preferredLocation,
                seeker.preferredWorkMode,
                skillsToText(seeker.skills),
                workExperiencesToText(seeker.workExperiences)
            ]
        ):
            continue

        if location and not containsText(seeker.preferredLocation, location):
            continue

        if workMode and not equalsText(seeker.preferredWorkMode, workMode):
            continue

        if education and not containsText(seeker.education, education):
            continue

        if minExperience is not None:
            if seeker.yearsOfExperience is None:
                continue

            if seeker.yearsOfExperience < int(minExperience):
                continue

        if skills and not matchesAnySkill(seeker.skills, skills):
            continue

        filteredSeekers.append(seeker)

    return filteredSeekers

def matchesKeywords(keywords, fields):
    keywordList = normalizeTerms(keywords)

    if not keywordList:
        return True

    searchableText = normalizeText("".join(
        str(field)
        for field in fields
        if field is not None
    ))

    for keyword in keywordList:
        if normalizeText(keyword) not in searchableText:
            return False

    return True

def matchesAnyKeyword(keywords, fields):
    keywordList = normalizeTerms(keywords)

    if not keywordList:
        return True

    searchableText = normalizeText("".join(
        str(field)
        for field in fields
        if field is not None
    ))

    for keyword in keywordList:
        if normalizeText(keyword) in searchableText:
            return True
    return False

def containsText(value, expected):
    if not expected:
        return True

    if value is None:
        return False

    return normalizeText(expected) in normalizeText(value)

def equalsText(value, expected):
    if not expected:
        return True

    if value is None:
        return False

    return normalizeText(value) == normalizeText(expected)

def matchesAnySkill(modelSkills, expectedSkills):
    expectedSkillNames = normalizeTerms(expectedSkills)

    if not expectedSkillNames:
        return True

    actualSkillNames = [
        normalizeText(skill.name)
        for skill in modelSkills
    ]

    for expectedSkill in expectedSkillNames:
        if normalizeText(expectedSkill) in actualSkillNames:
            return True

    return False

def normalizeTerms(value):
    if value is None:
        return []

    if isinstance(value, str):
        value = value.split(",")

    terms = []

    for item in value:
        if item is None:
            continue

        term = str(item).strip()

        if term:
            terms.append(term)

    return terms

def normalizeText(value):
    return str(value).strip().lower()

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