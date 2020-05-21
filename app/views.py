from app import app, login_manager
from flask import request, redirect, url_for, render_template,jsonify,session,make_response,g
from app.models import Users,Posts,Follows,Likes
from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import RegistrationForm,LoginForm,PostForm
from functools import wraps
import datetime
import os
import jwt





@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')



def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, 'some-secret')

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = data
    return f(*args, **kwargs)

  return decorated
    
@login_manager.user_loader
def load_user(id):
   return Users.query.get(int(id))

@app.route('/api/user/register', methods=['POST'])
def user_register():
    
        #request.headers['Content-Type'] = 'application/json'
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        passwordraw = request.form['password']
        email = request.form['email']
        location = request.form['location']
        bio = request.form['biography']
        date_joined = format_date_joined()

        try:
            photo = request.files['photo']
            if firstname == "" or lastname == ""  or username == "" or email == "" or photo.filename == "" or bio =="" or location=="" or email=="":
                return jsonify({'message':'Required Field is missing'})
        except:
            return jsonify({'message':'Please submit a profile photo'})
            
        try:
            if Users.query.filter_by(username=username).first() :
                return jsonify({'message':'Username taken'})
        except:
             print('Ok')
             
        filename = secure_filename(photo.filename)
        #photo.save(os.path.join("./app/static/uploads",filename))
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        password = generate_password_hash(passwordraw, method='sha256')
        
        #user = Users(firstname,lastname,email,username,location,password,bio,filename)
        user = Users(username, password, firstname, lastname, email, location, bio, filename,date_joined)            
        #print(user.get_id());
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message':'Sucessfully Registered'})


def format_date_joined():
    date_joined = datetime.datetime.now()
    return "Joined on " + date_joined.strftime("%B %m, %Y")
    

@app.route('/api/auth/login',methods=["POST"])
def login():
    error=None
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():

        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(user_name = username).first()

        if user and user.is_correct_password(password): 
            login_user(user)
            payload = {'id': current_user.id, 'username': current_user.user_name}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256') 
            return jsonify({'user_id': user_id, 'token':token,'message':'User successfully logged in!'})
        else:
            error = "Invalid email and/or password"
            return jsonify({'errors': error})
    else:
        return jsonify({'errors':form_errors(form)})
            
        

@app.route('/api/auth/logout', methods = ['GET'])
@login_required
@requires_auth
def logout():
    g.current_user = None
    return jsonify(message= 'You have successfully logged out')
    
        
@app.route('/api/posts', methods=['GET'])
@requires_auth
def api_posts():
   
    posts = Posts.query.all()
    
    if not posts:
        return jsonify({'message':'No post'})
            
    output = []
    
    for post in posts:
        postdata= {}
        
        poster =  Users.query.filter_by(id=post.user_id).first()
        likes  = Likes.query.filter_by(post_id=post.id).all()
        
        if not likes:
            postdata['no_of_likes'] = 0
        else:
            postdata['no_of_likes'] = len(likes)
            
        if not poster:
            postdata['username'] = "Anonymous"
            postdata['profile_pic'] = "anonymous.png"
        else:
             postdata['username'] = poster.username
             postdata['profile_pic'] = poster.profile_photo
             
        postdata['id'] = post.id
        postdata['user_id'] = post.user_id
        postdata['photo'] = post.photo
        postdata['caption'] = post.caption
        postdata['created_on'] = post.created_on[:-15]
        
        like = Likes.query.filter_by(user_id=int(g.current_user['user_id']),post_id=post.id).first()
        if like:
            postdata['liked'] = True
        else:
            postdata['liked'] = False
       
        output +=[postdata]
        
    return jsonify({'posts':output,'message':"All posts"})

@app.route('/api/users/<user_id>', methods=['GET'])
@requires_auth
def user(user_id): 
        _user_ = Users.query.filter_by(id=int(user_id)).first()
        followers = Follows.query.filter_by(user_id=int(user_id)).all()
        posts = Posts.query.filter_by(user_id=int(user_id)).all()
        
        userinfo={}
        userinfo['no_of_followers'] = len(followers)
        userinfo['no_of_posts'] = len(posts)
        
        for f in followers:
            if(g.current_user['user_id'] == f.follower_id ):
                userinfo['no_follow'] = False
                
        if userinfo.get('no_follow',None) == None:
            userinfo['no_follow'] = True
        user={}
        user['firstname'] = _user_.firstname
        user['lastname'] = _user_.lastname
        user['profile_photo'] = _user_.profile_photo
        user['location'] = _user_.location
        user['created_on'] = _user_.joined_on.strftime('%d, %b %Y')
        user['biography'] = _user_.biography
        
        return jsonify({'user':user,'userinfo':userinfo,'message':'sucess'})
    
    
    
@app.route('/api/users/<user_id>/posts', methods =['GET','POST'])
@requires_auth
def api_users_posts(user_id):
    
    if(request.method == "GET"):
        posts = Posts.query.filter_by(user_id=int(user_id)).all()
        
        if not posts:
            return jsonify({'message':'No post'})
        
        output = []
    
        for post in posts:
            postdata= {}
            postdata['id'] = post.id
            postdata['user_id'] = post.user_id
            postdata['photo'] = post.photo
            postdata['caption'] = post.caption
            postdata['created_on'] = post.created_on[:-15]
            
            postdata['liked'] = False
            
            output +=[postdata]
        return jsonify({'posts':output,'message':"All posts"})
    else:
        
        jsonify({'message': request.form['caption']})
        
        try:
            photo = request.files['photo']
        except:
            jsonify({'message':'Photo is missing'})
        
        if  not request.form['caption']:
            return jsonify({'message':'No Caption'}) 
         
         
        filename = secure_filename(photo.filename)
        photo.save(os.path.join("./app/static/img",filename))
        
        caption = request.form['caption']
        
        
        post = Posts(user_id=int(user_id),photo=filename,caption=caption)
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({'message':'sucess'})

@app.route('/api/users/<user_id>/follow', methods = ['POST'])
@requires_auth
def follow(user_id):
    
        follower_id = g.current_user['user_id']

        follow = Follows(user_id=int(user_id),follower_id=int(follower_id))
        
        db.session.add(follow)
        db.session.commit()
        
        return jsonify({'message':'sucess'})


# Like Route
@app.route('/api/posts/<post_id>/like',methods = ['POST'])
@requires_auth
def likes(post_id):
    
    like = Likes(user_id=g.current_user['user_id'],post_id=post_id)
    db.session.add(like)
    db.session.commit()
        
    return jsonify({'message':'sucess'})

def form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'danger')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
