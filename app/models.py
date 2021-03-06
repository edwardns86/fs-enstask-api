from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(300)) 
    name = db.Column(db.String(100), nullable = False)
    surname = db.Column(db.String(100))
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_id', backref=db.backref('assigned_user', lazy=True))
    created_tasks = db.relationship('Task', foreign_keys='Task.user_id', backref=db.backref('usertask_id', lazy=True))
    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in  self.__table__.columns}
class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref='token')

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, server_default="") 
    startdate = db.Column(db.DateTime, server_default=db.func.now())
    enddate = db.Column(db.DateTime, nullable=False)   
    tasks = db.relationship('Task', foreign_keys='Task.project_id', backref=db.backref("project", lazy=True))
    status= db.Column(db.String, server_default='Open')

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in  self.__table__.columns}

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, server_default="") 
    startdate = db.Column(db.DateTime, server_default=db.func.now())
    enddate = db.Column(db.DateTime, nullable=False)  
    project_id= db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id= db.Column(db.Integer, db.ForeignKey(User.id))
    assigned_id = db.Column(db.Integer, db.ForeignKey(User.id))
    status= db.Column(db.String, server_default='Open')
    
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in  self.__table__.columns}

# setup login manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# This reads header api token keys 
@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None

