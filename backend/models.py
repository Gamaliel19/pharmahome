from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(250), nullable=True)
    password = db.Column(db.String(300), nullable=False)
    products = db.relationship('Product', backref='user', lazy=True)

    def __init__(self, email, nom, prenom, password):
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.password = password

    def json(self):
        return {
            "email": self.email,
            "nom": self.nom,
            "prenom": self.prenom,
            "password": self.password
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    dosage = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    dateFabrication = db.Column(db.Date, nullable=False)
    dateExpiration = db.Column(db.Date, nullable=False)
    imageProduit = db.Column(db.LargeBinary, nullable=True)
    favori = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Assurez-vous que 'users.id' est correct
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nom, description, dosage, prix, quantite, categorie, dateFabrication, dateExpiration, imageProduit, favori, user_id):
        self.nom = nom
        self.description = description
        self.dosage = dosage
        self.prix = prix
        self.quantite = quantite
        self.categorie = categorie
        self.dateFabrication = dateFabrication
        self.dateExpiration = dateExpiration
        self.imageProduit = imageProduit
        self.favori = favori
        self.user_id = user_id

    def json(self):
        return {
            "nom": self.nom,
            "description": self.description,
            "dosage": self.dosage,
            "prix": self.prix,
            "quantite": self.quantite,
            "categorie": self.categorie,
            "dateFabrication": self.dateFabrication.strftime('%Y-%m-%d'),
            "dateExpiration": self.dateExpiration.strftime('%Y-%m-%d'),
            "imageProduit": self.imageProduit.decode('utf-8') if self.imageProduit else None,
            "favori": self.favori
        }
