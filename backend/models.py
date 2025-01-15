from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

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


class Product(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    nom = db.Column(db.String(300), nullable=False) 
    description = db.Column(db.Text) 
    prix = db.Column(db.Float) 
    quantite = db.Column(db.Integer, nullable=False) 
    categorie = db.Column(db.String(250))
    dateFabrication = db.Column(db.DateTime, nullable=False)  
    dateExpiration = db.Column(db.DateTime, nullable=False) 
    imageProduit = db.Column(db.String(200)) 
    favori = db.Column(db.Boolean, default=False) 

    def __init__(self,nom,description,prix,quantite,categorie,dateFabrication,dateExpiration,imageProduit,favori):
        self.nom = nom
        self.description = description
        self.prix = prix
        self.quantite = quantite
        self.categorie = categorie 
        self.dateFabrication = dateFabrication 
        self.dateExpiration = dateExpiration 
        self.imageProduit = imageProduit 
        self.favori = favori

    def json(self): 
        return {"nom":self.nom, "description": self.description, "prix":self.prix, "quantite":self.quantite, "categorie":self.categorie, "dateFabrication":self.dateFabrication, "dateExpiration":self.dateExpiration, "imageProduit":self.imageProduit, "favori":self.favori}
