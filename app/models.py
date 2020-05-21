from . import db
from werkzeug.security import generate_password_hash


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    caption = db.Column(db.String(255))
    created_on = db.Column(db.String(255))


    def __init__(self,userID,Photo,Caption,Created_on):
        self.user_id = userID
        self.photo = Photo
        self.caption = Caption
        self.created_on = Created_on

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
        
    def get_userId(self):
        try:
            return unicode(self.user_id)
        except NameError:
            return str(self.user_id)


    


class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    location = db.Column(db.String(255))
    biography = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    joined_on = db.Column(db.String(255))

    def __init__(self,Username,PW,firstName,lastName,email,loc,bio,pic,date_joined):
        self.id = 2;
        self.username = Username
        self.password = PW
        self.firstname = firstName
        self.lastname = lastName
        self.email = email
        self.location = loc
        self.biography = bio
        self.profile_photo = pic
        self.joined_on = date_joined

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Likes(db.Model):
    __tablename__ = 'Likes'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    def __init__(self, userID, postID):
        self.user_id = userID
        self.post_id = postID

    def get_postId(self):
        try:
            return unicode(self.post_id)
        except NameError:
            return str(self.post_id)
        
    def get_userId(self):
        try:
            return unicode(self.user_id)
        except NameError:
            return str(self.user_id)
        
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)


class Follows(db.Model):
    __tablename__ = 'Follows'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)

    def __init__(self, userID, followerID):
        self.user_id = userID
        self.follower_id = followerID

    def get_followerId(self):
        try:
            return unicode(self.follower_id)
        except NameError:
            return str(self.follower_id)
        
    def get_userId(self):
        try:
            return unicode(self.user_id)
        except NameError:
            return str(self.user_id)

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
