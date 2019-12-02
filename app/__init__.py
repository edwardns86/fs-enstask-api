from flask import Flask, redirect, url_for, flash, render_template, jsonify
from flask_login import login_required, logout_user , current_user, login_user
from .config import Config
from .models import db, login_manager , Token
from .oauth import blueprint
from .cli import create_db
from flask_migrate import Migrate
from flask_cors import CORS
import requests


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
    return redirect("https://localhost:3000/")
    

@app.route("/")
def index():
    return render_template("home.html")


@app.route('/login',methods=[ 'GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('events.home'))
    if request.method == "POST":
        user = User(email = request.json["email"]).check_user_email(request.json["email"])
        if not user: 
            flash("Your email is not registered",'warning')
            return redirect(url_for('users.register'))
        if user.check_password(request.json["password"]):   
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for('events.home'))
        flash('Incorrect password, please try to login again', 'warning')
    return render_template("views/login.html")    

@app.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect("https://localhost:3000/")
    if request.method == 'POST' :
        check_email = User.query.filter_by(email=request.json['email']).first() 
        if check_email:  
            flash('Email already taken', 'warning')
            return redirect(url_for('https://localhost:3000/login')) 
        if request.json['password'] != request.json['checkpassword']:
            flash('The passwords entered do not match', 'warning')
            return redirect(url_for('users.register'))
        new_user = User(name=request.json['name'],  
                        email=request.json['email'],
                        )
        new_user.generate_password(request.json['password'])  
        db.session.add(new_user) 
        db.session.commit() 
        login_user(new_user) 
        flash('Successfully created an account and logged in', 'success')
        return redirect(url_for('https://localhost:3000/')) # and redirect user to our root
    return render_template('https://localhost:3000/') 

@app.route('/getuserinfo', methods =['GET','POST']) 
@login_required
def getuser():  
    return jsonify({
        'success': True,
        'user_id': current_user.id,
        'user_name' :current_user.name
    })