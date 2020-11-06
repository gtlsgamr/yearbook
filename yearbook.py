from flask import request, jsonify
import os, json
from PIL import Image
import secrets
import sqlite3
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = '/static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yearbook.sqlite3'
cwd = os.getcwd()


SCHOOL_NAME='DPS'
db = SQLAlchemy(app)
class ybpic(db.Model):
    id = db.Column(db.Integer, primary_key='true')
    firstname = db.Column(db.String(15))
    lastname = db.Column(db.String(15))
    yb_pic = db.Column(db.String(16))
    yb_quote = db.Column(db.String(25))

    def __init__(self,firstname,lastname,yb_pic,yb_quote):
        self.firstname = firstname
        self.lastname = lastname
        self.yb_pic = yb_pic
        self.yb_quote = yb_quote

class confession(db.Model):
    confession = db.Column(db.String(200))
    id = db.Column(db.Integer, primary_key='true')

    def __init__(self, confession):
        self.confession = confession

class memory(db.Model):
    memory = db.Column(db.String(300))
    fullname = db.Column(db.String(30))
    id = db.Column(db.Integer, primary_key='true')

    def __init__(self, confession,fullname):
        self.memory = confession
        self.fullname = fullname
        
db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def homepage():
    return render_template('homepage.html', school_name=SCHOOL_NAME, title='Home')

@app.route('/yearbook', methods=['GET','POST'])
def yearbookpage():
    if request.method == 'POST':
        print("HGAHAHA")
        
        print(request.files.keys)
        file = request.files['yb_pic']
        name = secrets.token_urlsafe(16)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.split('.')[1]
            im = Image.open(file)
            im.thumbnail((500,500), Image.ANTIALIAS)
            im.save(f'{cwd}/static/images/people/{name}.{ext}')
            
        yb = ybpic(request.form['firstname'], request.form['lastname'], f'{name}.{ext}', request.form['yb_quote'])
        db.session.add(yb)
        db.session.commit()
        return render_template('yearbook.html', school_name=SCHOOL_NAME, title='Submit YB', message='Successful!')
    return render_template('yearbook.html', school_name=SCHOOL_NAME, title='Submit YB')

@app.route('/confession', methods=['GET','POST'])
def confession():
    if request.method == 'POST':
        c = confession(request.form['confession'])
        db.session.add(c)
        db.session.commit()
        return render_template('confessions.html', school_name=SCHOOL_NAME, title='Confession', message='Sucessful!')
    return render_template('confessions.html', school_name=SCHOOL_NAME, title='Confession')

@app.route('/writeup', methods=['GET','POST'])
def writeup():
    if request.method == 'POST':
        c = memory(request.form['memory'],request.form['fullname'])
        db.session.add(c)
        db.session.commit()
        return render_template('writeup.html', school_name=SCHOOL_NAME, title='Write-up', message='Sucessful!')
    return render_template('writeup.html', school_name=SCHOOL_NAME, title='Write-up')



if __name__ == "__main__":
    
    app.run(host="0.0.0.0")
