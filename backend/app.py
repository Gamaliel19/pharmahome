import os
from flask import Flask, redirect,request,jsonify, url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from flask_login import LoginManager, login_required, logout_user,login_user
from models import db, User
import re
from flask_jwt_extended import JWTManager, create_access_token,jwt_required
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
    email = request.json["email"]
    password=request.json["password"]
    user = User.query.filter_by(email=email).first() 
    if user:
        if bcrypt.check_password_hash(user.password, password):
            
            login_user(user)
            access_token = create_access_token(identity = user.id,expires_delta=timedelta(hours=24))
    
            return jsonify({'token' : access_token, 'userId': user.id,'userNom':user.nom + ' ' + user.prenom ,'userEmail':user.email}),200
        return ({"error":"Le mot de passe est incorrect! Renseigner bien le champ puis réessayer!"}),400
    return ({"error":"ce utilisateur n'existe pas! Veuillez créer un compte."}),401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('adminLogin'))

@app.route("/signupUser", methods=["POST"])
#@jwt_required()
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
@app.route('/listUser', methods=["GET"])
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
@app.route('/listSingleUser/<string:id>', methods= ['GET'])
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
