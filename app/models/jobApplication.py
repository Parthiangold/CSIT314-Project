from app.extensions import db

# Job Application Model
class JobApplication(db.Model):

    # Defines the table name
    __tablename__ = "jobApplications"

    # Unique Constraint to ensure that a user cannot apply for the same job twice
    __tabl_args__ = (
        db.UniqueConstraint(
            "seekerId",
            "jobPostingId",
            name="unique_application"
        ),
    )

    # Columns
    # PK for this object
    id = db.Column(db.Integer, primary_key=True)

    # FK to the SeekerProfile object
    seekerId = db.Column(
        db.Integer,
        db.ForeignKey("SeekerProfiles.id"),
        nullable=False
    )

    # FK to the JobPosting object
    jobPostingId = db.Column(
        db.Integer,
        db.ForeignKey("JobPostings.id"),
        nullable=False
    )

    # Updates the status of the job application
    status = db.Column(
        db.String(50),
        default="Pending"
    )

    # Date the application was submitted
    appliedDate = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # CV of the applicant
    cv = db.Column(db.Text)

    # Relationships
    seeker = db.relationship(
        "SeekerProfile",
        back_populates="jobApplications"
    )

    jobPosting = db.relationship(
        "JobPosting",
        back_populates="jobApplications"
    )