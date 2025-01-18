import os
from flask import Flask, redirect,request,jsonify, url_for
from flask_login import current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from flask_login import LoginManager, login_required, logout_user,login_user
from models import db, User, Product
import re
from flask_jwt_extended import JWTManager, create_access_token,jwt_required
from datetime import datetime
from werkzeug.security import check_password_hash
from datetime import timedelta



basedir = os.path.abspath(os.path.dirname(__file__))
app= Flask(__name__)

app.config["SECRET_KEY"] = "secret_key1234"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:''@localhost/pharmadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session(app)
jwt = JWTManager(app)

bcrypt=Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
with app.app_context():
    db.create_all()


#Commencent les routes pour le user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/loginUser', methods=['POST'])
def userLogin():
    email = request.json.get("email")
    password = request.json.get("password")
    
    if not email or not password:
        return jsonify({"error": "Veuillez fournir une adresse e-mail et un mot de passe."}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password): 
        login_user(user)
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))

        return jsonify({
            'token': access_token, 
            'userId': user.id, 
            'userNom': f"{user.nom} {user.prenom}", 
            'userEmail': user.email
        }), 200
    elif user:
        return jsonify({"error": "Le mot de passe est incorrect ! Renseignez bien le champ puis réessayez."}), 400
    else:
        return jsonify({"error": "Cet utilisateur n'existe pas ! Veuillez créer un compte."}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('userLogin'))

@app.route("/signupUser", methods=["POST"])
@jwt_required()
def register_user():
    email = request.json['email']
    nom = request.json['nom']
    prenom = request.json['prenom']
    password = request.json['password']

    user_exists=User.query.filter_by(email=email).first() is not None

    if user_exists:
        return ({"error" : "Cet utilisateur existe déjà!"}),408
    
    #admin_exist=User.query.filter_by(profil='admin').first() is not None
    regex_email = r'[a-z-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Z|a-z]{2,}'
    expression_compile=re.compile(regex_email)
    if not re.match(expression_compile, email):
        return ({"error":"L'email incorrect. Veuillez entrer le format valide!"}),413
    
    if len(password)<8:
        return ({"error":"Le mot de passe est trop court. Veuillez entrer au moins 8 caractères!"}),409
    
    elif not re.search("[0-9]",password):
        return ({"error":"Le mot de passe doit contenir au moins un chiffre!"}),410
    
    elif not re.search("[@#¦¬|¢´~}{)(:;.*-/+ %&ç$£äö><°§ ]",password):
        return ({"error":"Le mot de passe doit contenir au moins un caractère spécial!"}),411
    
    elif not re.search("[A-Z]",password):
        return jsonify({"error":"Le mot de passe doit contenir au moins une lettre majuscule!"}),412
    
    elif not re.search("[a-z]",password):
        return jsonify({"error":"Le mot de passe doit contenir au moins une lettre(minuscule)!"}),413
    

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, nom=nom, prenom=prenom, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {"Message": "Utilisateur créé avec succès!"}

#liste des utilisateurs
@app.route('/getUsers', methods=["GET"])
def list():
    users = User.query.all()
    liste=[]
    for user in users:
        data={}
        data['id']=user.id
        data['email'] = user.email
        data['nom'] = user.nom
        data['prenom'] = user.prenom
        liste.append(data)
    return jsonify(liste)

#obtenir un seul tilisateur
@app.route('/getUser/<string:id>', methods= ['GET'])
@jwt_required
def singleUser(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.json()
    return {'message': 'utilisateur non trouve'}

#supprimer un utilisateur 
@app.route('/deleteUser/<string:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': 'utilisateur supprime avec succes'}
    else:
        return {'message': 'utilisateur non trouve'}


#########################################   Manipulation de la classe produit  #####################################################

#Enregistrement d'un nouveau produit
@app.route('/registerProduct', methods=["POST"])
@jwt_required()  
def register_product():
    data = request.get_json()
    nom = data.get('nom')
    description = data.get('description')
    dosage = data.get('dosage')
    prix = data.get('prix')
    quantite = data.get('quantite')
    categorie = data.get('categorie')
    dateFabrication = data.get('dateFabrication')
    dateExpiration = data.get('dateExpiration')
    imageProduit = data.get('imageProduit').encode()
    favori = data.get('favori')

    if not nom:
        return jsonify({"error": "Veuillez entrer le nom du produit!"}), 405

    product = Product.query.filter_by(nom=nom, categorie=categorie, dosage=dosage, dateExpiration=dateExpiration).first()

    if product:
        product.quantite += int(quantite)
    else:
        product = Product(
            nom=nom,
            description=description,
            dosage=dosage,
            prix=prix,
            quantite=quantite,
            categorie=categorie,
            dateFabrication=datetime.strptime(dateFabrication, '%Y-%m-%d').strftime('%Y/%m/%d'),
            dateExpiration=datetime.strptime(dateExpiration, '%Y-%m-%d').strftime('%Y/%m/%d'),
            imageProduit=imageProduit,
            favori=favori,
            user_id=current_user.id  # Associe le produit à l'utilisateur actuel
        )
    
    db.session.add(product)
    db.session.commit()

    return jsonify(product.json()), 201


import base64

# Lister les produits
@app.route('/get_products', methods=['GET'])
def list_product():
    products = Product.query.order_by(Product.nom.asc()).all()
    liste = []
    for product in products:
        if product.quantite > 0:
            try:
                image_b64 = base64.b64encode(product.imageProduit).decode('utf-8') if product.imageProduit else None
            except Exception as e:
                print(f"Erreur lors de la conversion en base64: {e}")
                image_b64 = None

            data = {
                'id': product.id,
                'nom': product.nom,
                'description': product.description,
                'dosage': product.dosage,
                'prix': product.prix,
                'quantite': product.quantite,
                'categorie': product.categorie,
                'date_ajout': product.date_ajout.strftime("%d-%m-%Y"),
                'dateFabrication': product.dateFabrication.strftime("%d-%m-%Y"),
                'dateExpiration': product.dateExpiration.strftime("%d-%m-%Y"),
                'imageProduit': image_b64,
                'favori': product.favori
            }
            liste.append(data)
    return jsonify(liste)

# Suppression d'un produit
@app.route('/delete_product/<string:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Suppression réussie!'})
    else:
        return jsonify({'message': "Ce produit n'existe pas dans la base de données."})  # Correction de l'orthographe

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
