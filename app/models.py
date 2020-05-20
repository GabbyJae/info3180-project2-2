from werkzeug.security import generate_password_hash
from . import db
import datetime


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    caption = db.Column(db.String(255))
    created_on = db.Column(db.String(80))

    
    def __init__(self,user_id,photo,caption,created_on):
        #self.id = id
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
        self.created_on = created_on


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(255))
    location = db.Column(db.String(80))
    biography = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    
    def __init__(self, username, password, firstname, lastname, email, location, biography, photo):
        self.username = username
        self.password = generate_password_hash(password)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.photo = photo

    

class Likes(db.Model):
    __tablename__ = 'Likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    
    def __init__(self,post_id,user_id):
        self.user_id = user_id
        self.post_id = post_id
        
    
    
class Follows(db.Model):
    __tablename__ = 'Follows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)
    
    def __init__(self,user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id
    
def isfollowing(table,follower,following):
    flng = table.qutery.filter_by(username=follower).first().id
    flwr = table.qutery.filter_by(username=following).first().id
    for u in table.query.filter_by(follower=flng).all():
        if u == flwr:
            return True
    return False
    
def authenticate(table,username,password):
    user = table.query.filter_by(username=username)
    
    if user and safe_str_cmp(user.password.encode('utf-8'),password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return user_id.get(user_id, None)