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





MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')


@app.route('/login_admin',methods=['GET','POST'])
def login_admin():
    return render_template("login_admin.html")

@app.route("/login_user",methods=['GET','POST'])
def login_user():
    msg = request.args.get("msg")
    return render_template("login_user.html", msg=msg)
    
@app.route('/register',methods=['GET','POST'])
def register():
    return render_template("register.html")

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
@app.route("/home")
def home1():
    return render_template("home.html")





if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)