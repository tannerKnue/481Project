from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blindfold.db'
db = SQLAlchemy(app)
class profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    preference = db.Column(db.String(1), nullable=False)
    bio = db.Column(db.String(600), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<Name %r>' %self.id

    def to_json(self):
        return {
            "firstName":self.firstName,
            "lastName":self.lastName,
            "age":self.age,
            "gender":self.gender,
            "preference":self.preference,
            "bio":self.bio,
            "email":self.email,
            "username":self.username,
            "password":self.password   
        }
users = []

@app.route("/")
def loginPage():
    return render_template("login.html")

@app.route("/register")
def registerPage():
    return render_template("register.html")

@app.route("/profile", methods=["POST"])
def outputProfile():
    print("\n\n",request.form.get("firstName"),"\n\n")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    age = request.form.get("age")
    gender = request.form.get("gender")
    preference = request.form.get("preference")
    bio = request.form.get("bio")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    user = profiles(
        firstName=firstName,
        lastName=lastName,
        age=age,
        gender=gender,
        preference=preference,
        bio=bio,
        email=email,
        username=username,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return render_template("profile.html", firstName=firstName, lastName=lastName, age=age, gender=gender, preference=preference, email=email, username=username)

@app.route("/home")
def homePage():
    return render_template("home.html")

@app.route("/matches")
def matchesPage():
    return render_template("matches.html")

@app.route("/messages")
def messagesPage():
    return render_template("messages.html")

@app.route("/profile")
def profilePage():
    return render_template("profile.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = profiles.query.filter(profiles.username == username).first()
    if password == user.password:
        return render_template("profile.html",firstName=user.firstName, lastName=user.lastName, age=user.age, gender=user.gender, preference=user.preference, email=user.email, username=user.username)
    
    return user.to_json()

if __name__ == "__main__":
    app.run()
