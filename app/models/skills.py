from app.extensions import db

#Association Tables

seekerSkills = db.Table('seekerSkills',
                        db.Column('seekerId',
                                  db.Integer,
                                  db.ForeignKey('seekers.id'),
                                  primary_key=True
                        ),

                        db.Column(
                            'skillId',
                            db.Integer,
                            db.ForeignKey('skills.id'),
                            primary_key=True
                        )
                    )

jobSkills = db.Table('jobSkills',
                     db.Column('jobsId', db.Integer, db.ForeignKey('jobs.id'), primary_key=True),
                     db.Column('skillsId', db.Integer, db.ForeignKey('skills.id'), primary_key=True))

class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False)