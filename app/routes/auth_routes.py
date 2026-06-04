from flask import Blueprint, request, jsonify, make_response
from app.services import auth_service

authBp = Blueprint('auth', __name__, url_prefix='/api/auth')

@authBp.route('/register', methods=['POST'])
def register():

   data = request.get_json()

   result = auth_service.registerUser(
       email=data.get('email'),
       username=data.get('username'),
       password=data.get('password'),
       role=data.get('role')
   )

   status = 201 if result['success'] else 400

   return jsonify(result), status

@authBp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    result = auth_service.login(
        email=data.get('email'),
        password=data.get('password')
    )

    status = 200 if result['success'] else 401

    return jsonify(result), status