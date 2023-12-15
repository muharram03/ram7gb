from flask import Flask,redirect,url_for,render_template,request
from dotenv import load_dotenv

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')
@app.route('/login_admin')
def login_admin():
    return render_template("login_admin.html")

@app.route('/login_user')
def login_user():
    return render_template("login_user.html")
    
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/heroes')
def heroes():
    return render_template("heroes.html")

@app.route('/hero_story')
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





if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run("0.0.0.0", port=5000, debug=True)