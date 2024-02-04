from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)

# app.config.update(
#     MAIL_SERVER = "smtp.gmail.com",
#     MAIL_PORT = 465,
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail_ID'],
#     MAIL_PASSWORD = params['gmail_password']
# )
# mail = Mail(app)

local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_URI']

db = SQLAlchemy(app)


today = datetime.today()
year = today.year

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


@app.route("/")
def home():
    return render_template('index.html', param=params, year = year)


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

@app.route('/post/<string:post_slug>', methods = ['GET'])
def post_single(post_slug):

    post = All_posts.query.filter_by(slug = post_slug).first()
    return render_template('single-post.html', post= post, param=params, year = year)


app.run(debug=True)