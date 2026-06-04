from io import StringIO

from argon2 import PasswordHasher, verify_password
from argon2.exceptions import VerifyMismatchError

from app.models import SeekerProfile, EmployerProfile
from app.models.user import User
from app.extensions import db

ph = PasswordHasher()

def registerUser(email: str, username: str, password: str, role: str):

    if not email:
        return {
            "success": False,
            "message": "Email is required"
        }

    if not password:
        return {
            "success": False,
            "message": "Password is required"
        }

    passwordHash = ph.hash(password)

    existingUser = User.query.filter_by(
        email=email
    ).first()

    if existingUser:
        return {
            "success": False,
            "message": "User already exists"
        }

    newUser = User(
        email=email,
        username=username,
        passwordHash=passwordHash,
        role=role,
        hasMembership=False
    )

    if role == "SEEKER":
        seeker = SeekerProfile(
            user=newUser
        )
        db.session.add(seeker)

    elif role == "EMPLOYER":

        employer = EmployerProfile(
            user=newUser
        )
        db.session.add(employer)

    db.session.add(newUser)
    db.session.commit()

    return {
        "success": True,
        "message": "User created successfully",
        "userId": newUser.id
    }

def login(email: str, password: str):

    user = User.query.filter_by(email=email).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    try:
        ph.verify(password, user.passwordHash)

    except VerifyMismatchError:
        return {
            "success": False,
            "message": "Invalid password"
        }
    return {
        "success": True,
        "message": "Login successful",
        "userId": user.id,
        "hasMembership": user.hasMembership,
    }