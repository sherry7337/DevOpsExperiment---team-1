# Imports
import os
import sqlite3
from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import pandas as pd
import csv

# create the application object
app = Flask(__name__)

##################### Initiating the Database ########################
##Create Database from reading in the CSV file that we pulled from dataset one

df = pd.read_csv('data.csv')
df.columns = df.columns.str.strip()
connection = sqlite3.connect('demo.db')
df.to_sql('population', connection, if_exists='replace')
cursor = connection.cursor()


## Database 
sql_query = """SELECT * FROM population"""
cursor.execute(sql_query)
# Creating list from data in the DB
dataTest = [cursor.fetchall()]
#Printing list DataTest
print(dataTest)

##Attempting to ALTER the table to add a Meta Data column
# sql_alter = """ALTER TABLE population ADD COLUMN Meta_data char(255)"""
# cursor.execute(sql_alter)

# dataTest = [cursor.fetchall()]
# print(dataTest)


# LoginManager is needed for our application to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)


# Create User model for test.db Database
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(40), unique=True, nullable=False)
    #WFirstName = db.Column(db.String(20), nullable=False)
    #WLastName = db.Column(db.String(20), nullable=False)
    #WEmail = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.WFirstName}', '{self.WLastName}', '{self.WEmail}')"
 
# Initialize app with extension
db.init_app(app)
# Create database within app context

 
# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

#####################################################Decorators and Routes###############################################################
@app.route("/API/Login", methods=["GET", "POST"])
def api_login(WUserName, WPassword):
   usernameargs = request.args.get(WUserName)
   passwordargs = request.args.get(WPassword)
   print(usernameargs)
   print(passwordargs)

   dbpassword = dbquery("SELECT Password, FROM Users where username="+usernameargs+";")
   if passwordargs == dbpassword: 
       response = make_response({"data":dbpassword}, 200)
       print("good job")
       return response
   else:
       response = make_response({"data":"no"}, 400)
       print("go away")
       return response

@app.route("/API/Bulk")
def api_bulk():
    data = dbbulk()
    response = make_response({"data":data}, 200)
    return response

@app.route("/API/query")
def api_query():
    data = dbquery(request.args.get('country'))
    response = make_response({"data":data}, 200)
    return response

# Decorators are the names of URLS.
@app.route("/home", methods=["GET", "POST"])
def home():
    # Render home.html on "/home" route
    return render_template("home.html")

    #a second route to home without the need for a URL extension
@app.route("/", methods=["GET", "POST"])
def home2():
    # Render home.html on "/" route
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by filtering for the username
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("/API/Login"))
        # Redirect the user back to the home or "/"
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    if request.method == "POST":
        #takes the username and password entered by the users.
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        # Add the user to the DB
        db.session.add(user)
        # Commit the changes made to the DB
        db.session.commit()
        # Once user account is created, redirect them to the login page.
        return redirect(url_for("/home"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html")

#Signs the user out and returns them to the homepage
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


# method to display info from csv file
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    data = []
    with open('data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)

        return render_template('dashboard.html', data=data)


# method to access data.csv using json

#data for graph is being pulled from data.csv
#allows for the data to be used in a json format
@app.route('/data')
def get_data():
    data = []
    with open('data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    return jsonify(data)


#######################################################Start the server##############################################################
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

