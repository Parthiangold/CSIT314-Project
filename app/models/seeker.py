from app.extensions import db
from app.models.skills import seekerSkills

class Seeker(db.Model):
    __tablename__ = "seeker"

    id = db.Column(db.Integer, primary_key=True)

    userId = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        unique=True,
        nullable=False
    )

    education = db.column(db.String(255))

    major = db.column(db.String(255))

    fieldOfStudy = db.column(db.String(255))

    yearsOfExperience = db.column(db.Integer)

    preferredWorkMode = db.column(db.String(20))

    preferredLocation = db.column(db.String(100))

    # Relationships

    user = db.relationship(
        "User",
        back_populates="seekerProfile"
    )
    skills = db.relationship(
        "seekerSkills",
        secondary="seeker_skills",
        backref="seeker",

    )

    workExperiences = db.relationship(
        "WorkExperience",
        back_populates="seeker",
        cascade="all, delete-orphan"
    )
