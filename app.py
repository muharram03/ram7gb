import os
from os.path import join, dirname
from dotenv import load_dotenv
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app=Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

SECRET_KEY = "SPARTA"
TOKEN_KEY = 'mytoken'




MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

@app.route('/')
def main():
    return render_template("index.html" , active_page='home')

@app.route('/home')
def home():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("home.html" , active_page='home',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route('/login')
def login():
    return render_template("login.html")
    
@app.route('/register')
def register():
    return render_template("register.html" )

@app.route('/heroes')
def heroes():
    return render_template("heroes.html")

@app.route('/hero_story',methods=['GET'])
def hero_story():
    return render_template("hero_story.html")

@app.route('/skin')
def skin():
    return render_template("skin.html")

@app.route('/jungle')
def jungle():
    return render_template("jungle.html")

@app.route('/maps')
def maps():
    return render_template("interactive_.html")

@app.route('/discussion')
def discussion():
    return render_template("discussion.html")

@app.route('/discussion_reply')
def reply():
    return render_template("discussion_reply.html")

@app.route('/mypost')
def mypost():
    return render_template("mypost.html")

@app.route('/dahboard_discussion')
def dashboard_discussion():
    return render_template("dashboard_discussion.html")

@app.route('/dahboard_content')
def dashboard_content():
    return render_template("dashboard_content_heroes.html")

@app.route('/dahboard_heroes')
def dashboard_heroes():
    return render_template("dashboard_heroes.html")

@app.route('/dahboard_story')
def dashboard_story():
    return render_template("dashboard_hero_story.html")


@app.route('/sign_in', methods=['POST'])
def sign_in():
    email_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one({
            "email": email_receive,
            "password": pw_hash,
        })
    if result and 'admin' in result:
        payload = {
            "id": email_receive,
            "username": result['username'],
            "admin":True,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"result": "success", "token": token,})
    elif result and 'admin' not in result:
        payload = {
            "id": email_receive,
            "username": result['username'],
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"result": "success", "token": token,})
        
    # Let's also handle the case where the id and
    # password combination cannot be found
    else:
        return jsonify({"result": "fail","msg": "We could not find a user with that id/password combination",
            })
    
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form.get('username_give')
    email_recive = request.form.get('email_give')
    password_receive = request.form.get('password_give')
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # id
        "email" : email_recive,                                     # email
        "password": password_hash,                                  # password
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form.get('username_give')
    exists = bool(db.users.find_one({"email": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/profile/<keyword>')
def profile(keyword):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        
        return render_template("profile.html" ,user_info=payload)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))





if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)