from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyDTsLrpdTmRF3-M_91dx_mI_-MsAKK7Ge8",
    "authDomain": "first-project-c5adf.firebaseapp.com",
    "projectId": "first-project-c5adf",
    "storageBucket": "first-project-c5adf.appspot.com",
    "messagingSenderId": "712848640367",
    "appId": "1:712848640367:web:2c2ee803cfea4a431cc09a",
    "measurementId": "G-RVG8Q4GGWD",
    "databaseURL": "https://first-project-c5adf-default-rtdb.europe-west1.firebasedatabase.app"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except Exception as e:
            print(e)
            error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['full_name']
        username = request.form['username']     
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name" : name, "username" : username, "bio": bio, "email": email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        
        except Exception as e:
            print(e)
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        UID = login_session['user']['localId']
        try:
            tweet = {'text' : text, 'title': title, "uid": UID}
            db.child("Tweets").push(tweet)
        except:
            error = "problam publishing post"
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    return render_template('tweets.html', tweets = db.child("Tweets").get().val())

if __name__ == '__main__':
    app.run(debug=True)