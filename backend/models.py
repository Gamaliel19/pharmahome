from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(250))
    password = db.Column(db.String(300), nullable=False)

    def __init__(self, email, nom, prenom,password,):
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.password = password

    def json(self):
        return {"email":self.email, "nom":self.nom, "prenom":self.prenom, "password":self.password}

