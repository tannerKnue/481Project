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
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<Name %r>' %self.id

users = []

@app.route("/")
def loginPage():
    return render_template("login.html")

@app.route("/register")
def registerPage():
    return render_template("register.html")

@app.route("/profile", methods=["POST"])
def outputProfile():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    age = request.form.get("age")
    gender = request.form.get("gender")
    preference = request.form.get("preference")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    users.append(f"{firstName} {lastName} {age} {gender} {preference} {email} {username} {password}")
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

if __name__ == "__main__":
    app.run()
