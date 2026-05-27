from app.extensions import db
from app.models.skills import jobSkills

class JobPosting(db.Model):

    __tablename__ = "jobPostings"

    id = db.Column(db.Integer, primary_key=True)

    employerId = db.Column(
        db.Integer,
        db.ForeignKey('employerProfiles.id'),
        nullable=False
    )

    jobTitle = db.Column(
        db.String(255),
        nullable=False
    )

    companyInformation = db.Column(db.Text)

    jobDescription = db.Column(db.Text)

    requiredEducation = db.Column(
        db.String(255)
    )

    yearsOfExperience = db.Column(db.Integer)

    WorkMode = db.Column(db.String(20))

    jobLocation = db.Column(db.String(100))

    # Relationships
    employer = db.relationship(
        "EmployerProfile",
        back_populates="jobPostings"
    )

    jobSkills = db.relationship(
        "jobSkills",
        secondary=jobSkills,
        backref="jobPosting"
    )

    applications = db.relationship(
        "JobApplication",
        back_populates="jobPosting",
        cascade="all, delete-orphan"
    )