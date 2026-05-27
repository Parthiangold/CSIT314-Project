from app.extensions import db

class EmployerProfile(db.Model):
    __tablename__ = "employerProfiles"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        unique=True,
        nullable=False
    )

    companyName = db.Column(
        db.String(255),
        nullable=False
    )

    companyInformation = db.Column(db.Text)

    location = db.Column(db.String(100))

    # relationships
    user = db.relationship(
        "User",
        back_populates="employerProfile"
    )

    jobPosting = db.relationship(
        "Job",
        back_populates="employerProfile",
        cascade="all, delete-orphan"
    )