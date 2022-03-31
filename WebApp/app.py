from crypt import methods
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import wtforms, FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blindfold.db'
app.config['SECRET_KEY'] = 'secretKey'
db = SQLAlchemy(app)
class profiles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    preference = db.Column(db.String(1), nullable=False)
    bio = db.Column(db.String(600), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
class RegisterForm(FlaskForm):
    firstName = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "First Name"})
    lastName = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Last Name"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=16, max=40)], render_kw={"placeholder": "Password"})
    age = IntegerField(validators=[InputRequired()], render_kw={"placeholder":"Age"})
    gender = RadioField(validators=[InputRequired()],choices=[("Male"),("Female")])
    preference = RadioField(validators=[InputRequired()],choices=[("Male"),("Female")])
    bio = StringField(validators=[InputRequired(), Length(min=100, max=600)], render_kw={"placeholder": "Bio: Minimum 100 characters"})
    email = StringField(validators=[InputRequired(), Length(min=3, max=50)], render_kw={"placeholder": "Email"})
    
    submit = SubmitField("Register")
    
    def userValidation(self, username):
        existingUser = profiles.query.filter_by(username=username.data).first()
        if existingUser:
            raise ValidationError("That username is taken. Please choose a different one!")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=16, max=40)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")
    
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

@app.route("/login",methods=['GET','POST'])
def login():
    '''
    username = request.form.get("username")
    password = request.form.get("password")
    user = profiles.query.filter(profiles.username == username).first()
    if password == user.password:
        return render_template("profile.html",firstName=user.firstName, lastName=user.lastName, age=user.age, gender=user.gender, preference=user.preference, email=user.email, username=user.username)
    
    return user.to_json()
    '''
    form = LoginForm()
    return render_template('login.html', form=form)
    
@app.route("/register",methods=['GET','POST'])
def registerPage():
    form = RegisterForm()
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run()
