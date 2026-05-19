from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher

# shorthand variables for ease of use when importing to other python modules
db = SQLAlchemy()
argon = PasswordHasher()
