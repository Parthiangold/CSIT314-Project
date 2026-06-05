from .auth_routes import authBp
from .user_routes import userBp
from .employer_routes import employerBp
from .job_application_routes import jobApplicationBp
from .job_routes import jobBp
from .recommendation_routes import recommendationBp
from .search_routes import searchBp
from .seeker_routes import seekerBp

def registerBlueprints(app):
    app.register_blueprint(authBp)
    app.register_blueprint(userBp)
    app.register_blueprint(employerBp)
    app.register_blueprint(jobApplicationBp)
    app.register_blueprint(jobBp)
    app.register_blueprint(recommendationBp)
    app.register_blueprint(searchBp)
    app.register_blueprint(seekerBp)