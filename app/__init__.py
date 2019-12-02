from flask import Flask, redirect, url_for, flash, render_template, jsonify, request
from flask_login import login_required, logout_user , current_user, login_user
from .config import Config
from .models import db, login_manager , Token, User
from .oauth import blueprint
from .cli import create_db
from flask_migrate import Migrate
from flask_cors import CORS
import requests, uuid


app = Flask(__name__)

app.config.from_object(Config)
print(app.config['SQLALCHEMY_DATABASE_URI']) 
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)
db.init_app(app)

migrate=Migrate(app,db)

login_manager.init_app(app)
CORS(app)

@app.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id=current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    logout_user()
    flash("You have logged out")
    return jsonify({
        'success':True,
    })
    

@app.route("/")
def index():
    return render_template("home.html")


@app.route('/login',methods=[ 'GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user: 
            return jsonify({
                           "success":False,
                "message":"No User"
            })
        if user.check_password(data["password"]):   
            token = Token.query.filter_by(user_id=user.id).first()
            if not token:
                token = Token(user_id=user.id, uuid=str(uuid.uuid4().hex))
                db.session.add(token)
                db.session.commit()
            login_user(user)
    return jsonify({
        "success":True,
        "user":{
                        'user_id': current_user.id,

            "name":user.name
        },
        "token": token.uuid
    })

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST' :
        data = request.get_json()
        check_email = User.query.filter_by(email=data['email']).first() 
        if check_email:  
            return jsonify({
                "success":False,
                "message":"Email taken"
            })
       
        new_user = User(name=data['name'],  
                        email=data['email'],
                        )
        new_user.generate_password(data['password'])  
        db.session.add(new_user) 
        db.session.commit() 
    return jsonify({
                    "success":True
    }) 
        # and redirect user to our root

@app.route('/getuserinfo', methods =['GET']) 
@login_required
def getuser():  
    print('adsadasdasdasdsa')
    return jsonify({
        'success': True,
        'user':{
            'user_id': current_user.id,
        'name' :current_user.name
        },
        'token' : current_user.token[0].uuid
    })