from app.extensions import db

class WorkExperience(db.Model):

    __tablename__ = "work_experiences"

    id = db.Column(db.Integer, primary_key=True)

    seekerId = db.Column(
        db.Integer,
        db.ForeignKey('seekerProfiles.id'),
        nullable=False
    )

    workPlaceName = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(100),
        nullable=False
    )

    yearDuration = db.Column(db.Integer)

    # Relationships
    seeker = db.relationship(
        "SeekerProfile",
        back_populates="workExperiences"
    )
