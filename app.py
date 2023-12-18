from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from os.path import join, dirname
from dotenv import load_dotenv


app=Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

MONGODB_CONNECTION_STRING = "mongodb://Idrzne:arya@ac-hgdb3fh-shard-00-00.nasd6qr.mongodb.net:27017,ac-hgdb3fh-shard-00-01.nasd6qr.mongodb.net:27017,ac-hgdb3fh-shard-00-02.nasd6qr.mongodb.net:27017/?ssl=true&replicaSet=atlas-ccdo0u-shard-0&authSource=admin&retryWrites=true&w=majority"
DB_NAME =  "testfp"
SECRET_KEY = "arya"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client[DB_NAME]


@app.route("/")
def home():
    msg = request.args.get("msg")
    return render_template("index.html", msg=msg)

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template("login.html", msg=msg)
    
@app.route("/discussion")
def discussion():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('discussion.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("home", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("home", msg="There was problem logging you in"))

    
@app.route("/posting", methods=["POST"])
def posting():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here
        user_info = db.users.find_one({"username": payload["id"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "date": date_receive,
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", "msg": "Posting successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("discussion"))
    
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
        return redirect(url_for("discussion"))

# @app.route("/sign_in", methods=["POST"])
# def sign_in():
#     # Sign in
#     username_receive = request.form["username_give"]
#     password_receive = request.form["password_give"]
#     pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
#     result = db.users.find_one(
#         {
#             "username": username_receive,
#             "password": pw_hash,
#         }
#     )
#     if result:
#         payload = {
#             "id": username_receive,
#             # the token will be valid for 24 hours
#             "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

#         return jsonify(
#             {
#                 "result": "success",
#                 "token": token,
#             }
#         )
#     # Let's also handle the case where the id and
#     # password combination cannot be found
#     else:
#         return jsonify(
#             {
#                 "result": "fail",
#                 "msg": "We could not find a user with that id/password combination",
#             }
#         )
    
# @app.route("/discussion")
# def discussion():
#     # token_receive = request.cookies.get("mytoken")
#     # try:
#     #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
#     #     user_info = db.users.find_one({"username": payload["id"]})
#     #     return render_template('discussion.html', user_info=user_info)
#     # except jwt.ExpiredSignatureError:
#     #     return redirect(url_for("login", msg="Your token has expired"))
#     # except jwt.exceptions.DecodeError:
#     #     return redirect(url_for("login", msg="There was problem logging you in"))
#     return render_template('discussion.html')


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run("0.0.0.0", port=5000, debug=True)