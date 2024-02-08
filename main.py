from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
# from flask_mail import Mail
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email, DataRequired, EqualTo
from flask_bcrypt import Bcrypt


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = "Your_secret_string"



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"


bycrpt  = Bcrypt(app)


local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_URI']

db = SQLAlchemy(app)


today = datetime.today()
year = today.year

@login_manager.user_loader
def load_user(user_id):
    return All_users.query.get(int(user_id))


class Contact_form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(30), nullable=False)

class All_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(50), nullable=False)
    post_content = db.Column(db.String(130), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    img_file = db.Column(db.String(15), nullable=False)

class All_users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(30), nullable=False)

class RegisterationFrom(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=40)], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField("password",validators=[InputRequired(), EqualTo('confirm_password', message='Passwords Must Match!'), Length(min=5, max=225)], render_kw={"class": "form-control"})
    confirm_password = PasswordField("Comfirm Password",validators=[InputRequired() ,Length(min=5, max=225)], render_kw={"class": "form-control"})
    submit = SubmitField("Register", render_kw={"class": "btn btn-primary btn-lg"})

    def validate_email(self, email):
        existing_email = All_users.query.filter_by(email=email.data).first()
        if existing_email:
            flash('Email already registered')
            raise ValidationError('Email already registered')

class LoginFrom(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min= 1, max=40)], render_kw = {"class":"form-control mb-3", "placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min= 5, max=225)], render_kw = {"class":"form-control", "placeholder":"Password"})
    submit = SubmitField("Login", render_kw = {"class":"btn btn-primary btn-lg"})


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterationFrom()
    if form.validate_on_submit():
        password_hashed = bycrpt.generate_password_hash(form.password.data)
        new_user = All_users( name= form.name.data, email = form.email.data, password = password_hashed, date=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template('register.html', param= params, year = year, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = All_users.query.filter_by(email = form.email.data).first()
        if user:
            if bycrpt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("login successfully!!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password try again")
        else:
            flash("User Doesn't Exists!!")
    return render_template('login.html', param=params, year=year, form= form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    get_users = All_users.query.filter_by().all()
    formatted_posts = []
    for post in get_users:
        formatted_date = post.date.strftime("%B %d, %Y %H:%M:%S")
        formatted_posts.append((post, formatted_date))
    return render_template('dashboard.html', param=params, year=year, get_users=get_users, formatted_date= formatted_date)


@app.route("/")
def home():
    post_data = All_posts.query.filter_by().all()
    formatted_posts = []
    for post in post_data:
        formatted_date = post.date.strftime("%B %d, %Y")
        formatted_posts.append((post, formatted_date))
    return render_template('index.html', param=params, year=year, post=formatted_posts[0:2])  #formatted_posts[0:2] is used for post per page


@app.route('/about')
def about():
    return render_template('about.html', param=params, year = year)


@app.route('/post')
def sample_post():
    return render_template('post.html', param=params, year = year)

@app.route('/contact-us', methods = ['GET','POST'])
def contact_us():
    if(request.method == 'POST'):
        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')

        all_entries = Contact_form(name=name, email=email, phone_number=phone_number, message=message, date=datetime.now())
        db.session.add(all_entries)
        db.session.commit()
        # mail.send_message(
        #     "New Message From " + name,
        #     sender = email,
        #     recipients = [params['gmail_ID']],
        #     body = message + "\n" + phone_number
        # )

    return render_template('contact.html', param=params, year = year)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_single(post_slug):
    post = All_posts.query.filter_by(slug=post_slug).first()

    if not post:
        return render_template('404.html', param=params, year=year), 404

    formatted_date = post.date.strftime("%B %d, %Y")
    return render_template('single-post.html', post=post, formatted_date=formatted_date, param=params, year=year)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', param=params, year=year), 404




app.run(debug=True)
