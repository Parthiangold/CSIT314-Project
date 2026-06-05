from app.extensions import db
from app.models import SeekerProfile, Skill, User, WorkExperience

def serializeSkills(skill):
    return {
        "id": skill.id,
        "name": skill.name
    }

def serializeWorkExperience(workExperience):
    return {
        "id": workExperience.id,
        "workPlaceName": workExperience.workPlaceName,
        "role": workExperience.role,
        "yearDuration": workExperience.yearDuration,
    }

def serializeSeekerProfile(seekerProfile):
    return {
        "id": seekerProfile.id,
        "userId": seekerProfile.user.id,
        "fullName": seekerProfile.fullName,
        "contact": seekerProfile.pNumber if seekerProfile.user else None,
        "email": seekerProfile.user.email if seekerProfile.user else None,
        "education": seekerProfile.education,
        "major": seekerProfile.major,
        "fieldOfStudy": seekerProfile.fieldOfStudy,
        "yearsOfExperience": seekerProfile.yearsOfExperience,
        "preferredWorkMode": seekerProfile.preferredWorkMode,
        "preferredLocation": seekerProfile.preferredLocation,
        "skills": [serializeSkills(skill) for skill in seekerProfile.skills],
        "workExperiences": [serializeWorkExperience(workExperience) for workExperience in seekerProfile.workExperiences],
    }

def getAllSeekers():
    seekers = SeekerProfile.query.all()
    return {
        "success": True,
        "seekers": [serializeSeekerProfile(seeker) for seeker in seekers]
    }

def getSeekerById(seekerId):
    seeker = SeekerProfile.query.get(seekerId)

    if not seeker:
        return {
            "success": False,
            "message": "Seeker profile not found"
        }
    return {
        "success": True,
        "seeker": serializeSeekerProfile(seeker)
    }

def getSeekerByUserId(userId):
    seeker = SeekerProfile.query.filter_by(userId=userId).first()

    if not seeker:
        return {
            "success": False,
            "message": "Seeker profile not found"
        }
    return {
        "success": True,
        "seeker": serializeSeekerProfile(seeker)
    }

def saveSeekerProfile(userId, data):
    user = User.query.get(userId)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if user.userType != "candidate":
        return {
            "success": False,
            "message": "User is not a candidate"
        }

    seeker = SeekerProfile.query.filter_by(userId=userId).first()

    if not seeker:
        seeker = SeekerProfile(userId=userId)
        db.session.add(seeker)

    seeker.fullName = data.get("fullName", seeker.fullName)
    seeker.education = data.get("education", seeker.education)
    seeker.major = data.get("major", seeker.major)
    seeker.fieldOfStudy = data.get("fieldOfStudy", seeker.fieldOfStudy)
    seeker.yearsOfExperience = data.get("yearsOfExperience", seeker.yearsOfExperience)
    seeker.preferredWorkMode = data.get("preferredWorkMode", seeker.preferredWorkMode)
    seeker.preferredLocation = data.get("preferredLocation", seeker.preferredLocation)

    if "contact" in data:
        user.pNumber = data.get("contact")

    if "skills" in data:
        seeker.skills = buildSkillList(data.get("skills"))

    if "workExperiences" in data:
        seeker.workExperiences = buildWorkExperienceList(
            data.get("workExperiences")
        )

    db.session.commit()

    return {
        "success": True,
        "message": "Seeker profile saved successfully",
        "seeker": serializeSeekerProfile(seeker)
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

def buildWorkExperienceList(rawWorkExperiences):
    if not isinstance(rawWorkExperiences, list):
        return []

    workExperiences = []

    for item in rawWorkExperiences:
        if not isinstance(item, dict):
            continue

        workPlaceName = item.get("workPlaceName")
        role = item.get("role")

        if not workPlaceName or not role:
            continue

        workExperiences.append(
            WorkExperience(
                workPlaceName=workPlaceName,
                role=role,
                yearDuration=item.get("yearDuration")
            )
        )

    return workExperiences