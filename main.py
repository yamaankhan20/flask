from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/tech_blogs'
# db = SQLAlchemy(app)
@app.route("/")
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post')
def sample_post():
    return render_template('post.html')

@app.route('/contact-us')
def contact_us():
    return render_template('contact.html')

app.run(debug=True)