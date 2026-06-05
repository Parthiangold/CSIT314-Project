from io import StringIO

from argon2 import PasswordHasher, verify_password
from argon2.exceptions import InvalidHashError, VerifyMismatchError

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

    if not username:
        return {
            "success": False,
            "message": "Username is required"
        }

    normalizedRole = role.lower() if role else ""
    if normalizedRole not in ("candidate", "employer"):
        return {
            "success": False,
            "message": "Role must be candidate or employer"
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
        userName=username,
        passwordHash=passwordHash,
        userType=normalizedRole,
        isMember=False
    )

    if normalizedRole == "candidate":
        seeker = SeekerProfile(
            user=newUser,
            fullName=username
        )
        db.session.add(seeker)

    elif normalizedRole == "employer":

        employer = EmployerProfile(
            user=newUser,
            companyName=username
        )
        db.session.add(employer)

    db.session.add(newUser)
    db.session.commit()

    return {
        "success": True,
        "message": "User created successfully",
        "userId": newUser.id,
        "role": newUser.userType,
        "isMember": newUser.isMember
    }

def login(email: str, password: str):

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

    user = User.query.filter_by(email=email).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    try:
        ph.verify(user.passwordHash, password)

    except (InvalidHashError, VerifyMismatchError):
        return {
            "success": False,
            "message": "Invalid password"
        }
    return {
        "success": True,
        "message": "Login successful",
        "userId": user.id,
        "username": user.userName,
        "role": user.userType,
        "isMember": user.isMember,
    }
