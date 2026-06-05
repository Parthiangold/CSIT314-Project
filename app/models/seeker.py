from app.extensions import db
from app.models.skills import seekerSkills

class SeekerProfile(db.Model):
    __tablename__ = "seekerProfiles"

    id = db.Column(db.Integer, primary_key=True)

    userId = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        unique=True,
        nullable=False
    )

    fullName = db.Column(
        db.String(255),
        nullable=True
    )

    education = db.Column(db.String(255))

    major = db.Column(db.String(255))

    fieldOfStudy = db.Column(db.String(255))

    yearsOfExperience = db.Column(db.Integer)

    preferredWorkMode = db.Column(db.String(20))

    preferredLocation = db.Column(db.String(100))

    # Relationships

    user = db.relationship(
        "User",
        back_populates="seekerProfile"
    )
    skills = db.relationship(
        "Skill",
        secondary=seekerSkills,
        back_populates="seekers",

    )

    workExperiences = db.relationship(
        "WorkExperience",
        back_populates="seeker",
        cascade="all, delete-orphan"
    )

    jobApplications = db.relationship(
        "JobApplication",
        back_populates="seeker",
        cascade="all, delete-orphan"
    )
