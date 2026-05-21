from app.extensions import db

class User(db.Model):

    # __tablename__ defines the actual name of the relational table for SQLite
    __tablename__ = "users"

    # Column
    # id is the primary key for this table
    id = db.Column(db.Integer, primary_key=True)

    # creates a column populated with the actual name of the Users and doesn't accept null values.
    fullName = db.Column(
        db.String(255),
        nullable=False
    )

    # creates a column populated with the email of the users,
    # doesn't accept null values, and is a unique candidate key.
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    passwordHash = db.Column(
        db.String(255),
        nullable=False
    )

    pNumber = db.Column(
        db.String(255),
        nullable=False
    )

    userType = db.Column(
        db.String(20),
        nullable=False
    )

    isMember = db.Column(
        db.Boolean,
        default=False
    )

    #Association Tables
    #Relationships
    #uselist=False means that there can only be one of these relationships
    seekerProfile = db.relationship(
        "SeekerProfile",
        backref="user",
        uselist=False
    )

    employerProfile = db.relationship(
        "EmployerProfile",
        backref="user",
        uselist=False
    )