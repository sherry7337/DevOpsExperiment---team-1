## Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
##from flask_bcyrpt import Bcyrpt
##from flask_login import LoginManager

app = Flask(__name__)
app.debug = True

## Configuration settings for Database - sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

## Creation of SQLAlchemy instance
db = SQLAlchemy(app)

#login_manager = LoginManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', {self.email})"



@app.route("/")
def hello_world():
    return "<p>Flask is Working</p>"


if __name__ == '__main__':
    app.run()