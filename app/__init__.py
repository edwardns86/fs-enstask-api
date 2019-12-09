from flask import Flask, redirect, url_for, flash, render_template, jsonify, request
from flask_login import login_required, logout_user , current_user, login_user
from .config import Config
from .models import db, login_manager , Token, User ,Project, Task
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
    return jsonify({
        'success': True,
        'user':{
            'user_id': current_user.id,
        'name' :current_user.name
        },
        'token' : current_user.token[0].uuid
    })

@app.route('/newproject', methods =['POST'])

def createproject():
    if request.method == 'POST' :
        data = request.get_json()
        new_project = Project (
            title = data['title'],
            description = data['description'],
            startdate = data['startdate'],
            enddate = data['enddate']
        )
        db.session.add(new_project) 
        db.session.commit() 
    return jsonify({
                    "success":True
    }) 

@app.route('/getprojects')
@login_required
def getprojects():
    projects= Project.query.all()
    jsonised_object_list = []
    for project in projects:
        jsonised_object_list.append(project.as_dict())
    return jsonify(jsonised_object_list)


@app.route('/getusers')
@login_required
def getuserss():
    users= User.query.all()
    jsonised_object_list = []
    for user in users:
        jsonised_object_list.append(user.as_dict())
    return jsonify(jsonised_object_list)
                    
@app.route('/project/<id>')
@login_required
def showproject(id):
    project = Project.query.filter_by(id=id).first()
    print("PROJECT: ", project)
    tasks = Task.query.filter_by(project_id=project.id).all()
    
    jsonised_object_list = []
    if not tasks:
        jsonised_object_list.append(project.as_dict())
        return jsonify({
            'success': True,
            'project' :{
                'id': project.id,
                'title': project.title,
                'description': project.description
            }})
    for task in tasks :
        # import code; code.interact(local=dict(globals(), **locals()))
        if task.assigned_id:
            new_task = task.as_dict()
            new_task['assignee'] = User.query.filter_by(id=task.assigned_id).all()[0].as_dict()
        else:
            new_task = task.as_dict()
        jsonised_object_list.append(new_task)
    return jsonify({
            'success': True,
            'project': {
                'id': project.id,
                'title': project.title,
                'description': project.description,
            },
            'tasks': jsonised_object_list
            }) 

@app.route('/tasks', methods =['POST'])
@login_required
def createtask():
    id = request.get_json()['id']
    
    if request.method == 'POST' :
        data = request.get_json()
        print(data)
        new_task = Task (
            title = data['input']['title'],
            description = data['input']['description'],
            startdate = data['input']['startdate'],
            enddate = data['input']['enddate'],
            user_id = current_user.id,
            assigned_id = data['input']['assigned_id'],
        )
        project = Project.query.filter_by(id = id).first() 
        if project :
            new_task.project_id = project.id
        db.session.add(new_task) 
        db.session.commit() 
    return jsonify({
                    "success":True
    }) 

@app.route('/edittasks', methods = ['POST'])
@login_required
def edittask():
    
    id = request.get_json()['id']
    task = Task.query.filter_by(id=id).first()
    if request.method == 'POST' :
        data = request.get_json()
        print(data)
        task.title = data['input']['title'],
        task.description = data['input']['description'],
        task.status = data['input']['status'],
        task.assigned_id = data['input']['assigned_id']
        task.startdate = data['startDate'],
        task.enddate = data['endDate'],
        db.session.commit()
    return jsonify({
                    "success":True


    }) 
