from app.extensions import db
from app.models import User


def serializeUser(user):
    return {
        "id": user.id,
        "userName": user.userName,
        "email": user.email,
        "pNumber": user.pNumber,
        "userType": user.userType,
        "isMember": user.isMember,
        "seekerProfileId": user.seekerProfile.id
        if user.seekerProfile else None,
        "employerProfileId": user.employerProfile.id
        if user.employerProfile else None
    }

def getAllUsers():
    users = User.query.all()

    return {
        "success": True,
        "users": [serializeUser(user) for user in users]
    }

def getUserById(userId):
    user = User.query.get(userId)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    return {
        "success": True,
        "user": serializeUser(user)
    }

def updateUser(userId, data):
    user = User.query.get(userId)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    user.userName = data.get("userName", user.userName)
    user.pNumber = data.get("pNumber", user.pNumber)

    if "isMember" in data:
        user.isMember = bool(data.get("isMember"))

    db.session.commit()

    return {
        "success": True,
        "message": "User updated successfully",
        "user": serializeUser(user)
    }

def updateMembership(userId, isMember):
    user = User.query.get(userId)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    user.isMember = bool(isMember)
    db.session.commit()

    return {
        "success": True,
        "message": "Membership status updated successfully"
    }

def deleteUser(userId):
    user = User.query.get(userId)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    db.session.delete(user)
    db.session.commit()

    return {
        "success": True,
        "message": "User deleted successfully"
    }