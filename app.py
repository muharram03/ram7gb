import os
from os.path import join, dirname
from bson import ObjectId
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
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("heroes.html" , active_page='heroes',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/hero_story',methods=['GET'])
def hero_story():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("hero_story.html" , active_page='hero_story',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/skin')
def skin():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("skin.html" , active_page='skin',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/jungle')
def jungle():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("jungle.html" , active_page='jungle',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/interactive_maps')
def maps():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("interactive_maps.html" , active_page='interactive_maps',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/discussion')
def discussion():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("discussion.html" , active_page='discussion',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route("/posting", methods=["POST"])
def posting():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        print(payload)
        # We should create a new post here
        user_info = db.users.find_one({"username": payload["username"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        doc = {
            "username": user_info["username"],
            "comment": comment_receive,
            "date": date_receive,
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", "msg": "Posting successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/edit/<id>", methods=["POST"])
def edit(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here
        user_info = db.users.find_one({"username": payload["username"]})
        username = user_info["username"]
        comment_receive = request.form["comment_give"]
        doc = {
            "comment": comment_receive,
        }
        result = db.posts.update_one({"_id": ObjectId(id)}, {"$set": doc})
        return jsonify({"result": "success", "msg": "Posting successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/edit_heroes/<id>", methods=["POST"])
def edit_heroes(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here
        user_info = db.users.find_one({"username": payload["username"]})
        username = user_info["username"]
        
        heroes = request.form["hero"]
        role = request.form["roles"]
        doc = {
            "heroes": heroes,
            "roles": role
        }
        if 'icon' in request.files:
            icon = request.files["icon"]
            filename = secure_filename(icon.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{filename}.{extension}"
            icon.save("./static/" + file_path)
            doc["icon"] = file_path

        db.heroes.update_one({"_id": ObjectId(id)}, {"$set": doc})
        return jsonify({"result": "success", "msg": "Edit successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/hapus/<id>", methods=["POST"])
def hapus(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here

        db.posts.delete_one({"_id": ObjectId(id)})
        return jsonify({"result": "success", "msg": "Delete successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/hapus_heroes/<id>", methods=["POST"])
def hapus_heroes(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here

        db.heroes.delete_one({"_id": ObjectId(id)})
        return jsonify({"result": "success", "msg": "Delete successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get_posts", methods=["GET"])
def get_posts():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])

        username_receive = request.args.get("username_give")
        if username_receive == "":
            posts = list(db.posts.find({}).sort("date", -1).limit(20))
        else:
            posts = list(
                db.posts.find({"username": username_receive}).sort("date", -1).limit(20)
            )

        for post in posts:
            post["_id"] = str(post["_id"])
            post["count_heart"] = db.likes.count_documents(
                {"post_id": post["_id"], "type": "heart"}
            )
            post["count_star"] = db.likes.count_documents(
                {"post_id": post["_id"], "type": "star"}
            )            
            post["count_thumbsup"] = db.likes.count_documents(
                {"post_id": post["_id"], "type": "thumbsup"}
            )            
            
            post["heart_by_me"] = bool(
                db.likes.find_one(
                    {"post_id": post["_id"], "type": "heart", "username": payload["id"]}
                )
            )
            post["star_by_me"] = bool(
                db.likes.find_one(
                    {"post_id": post["_id"], "type": "star", "username": payload["id"]}
                )
            )
            post["thumbsup_by_me"] = bool(
                db.likes.find_one(
                    {"post_id": post["_id"], "type": "thumbsup", "username": payload["id"]}
                )
            )

        return jsonify(
            {
                "result": "success",
                "msg": "Successful fetched all posts",
                "posts": posts,
            }
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/get_heroes')
def get_heroes():
    heroes = list(db.heroes.find({}))
    for hero in heroes:
        hero['_id'] = str(hero['_id'])
    return jsonify({"result": "success", "heroes": heroes})

@app.route('/discussion_reply')
def reply():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("skin.html" , active_page='skin',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/mypost')
def mypost():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        username = payload["username"]
        status = username == payload["id"]
        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template("mypost.html" , active_page='mypost',user_info=user_info, status=status)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/dashboard_discussion')
def dashboard_discussion():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )

        # Check if the user has the "admin" role
        if 'admin' in payload.get('roles', []):
            return render_template("dashboard_discussion.html", active_page='dashboard_discussion', user_info=payload)
        else:
            return redirect(url_for('home', msg='You are not admin'))
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/dahboard_content')
def dashboard_content():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("dashboard_content.html" , active_page='dashboard_content',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/dashboard_heroes')
def dashboard_heroes():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("dashboard_heroes.html" , active_page='dashboard_heroes',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))
    

@app.route('/tambah', methods=["POST"])
def tambah():
    token_receive = request.cookies.get(TOKEN_KEY)
    icon = request.files["icon"]
    heroes = request.form["hero"]
    role = request.form["roles"]
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        doc = {
            "heroes": heroes,
            "roles": role
        }
        filename = secure_filename(icon.filename)
        extension = filename.split(".")[-1]
        file_path = f"profile_pics/{filename}.{extension}"
        icon.save("./static/" + file_path)
        doc["icon"] = file_path

        db.heroes.insert_one(doc)
        return jsonify({"result": "success", "msg": "Heroes updated!"})
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route('/dashboard_story')
def dashboard_story():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        print(payload)
        if 'admin' in payload:
            return render_template("dashboard.html", user_info=payload)
        else:
            return redirect(url_for('/home', msg='You are not admin'))
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    email_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    result = db.users.find_one({
        "email": email_receive,
        "password": pw_hash,
    })

    if result:
        payload = {
            "id": email_receive,
            "username": result['username'],
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }

        if result["roles"] == 'admin':
            payload["admin"] = True

           
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # Arahkan ke halaman dashboard jika admin berhasil login
            return jsonify({"result": "success", "token": token, "admin": True})

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        print(token)
        return jsonify({"result": "success", "token": token})
    
    return jsonify({"result": "failure", "message": "Invalid credentials"})
    
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
        "roles":"user",
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