from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

Config = {
  'apiKey': "AIzaSyCButbubOaVc-H8ON2SFLXsmx1UvQ2pQdQ",
  'authDomain': "yoyo2-ac013.firebaseapp.com",
  'projectId': "yoyo2-ac013",
  'storageBucket': "yoyo2-ac013.appspot.com",
  'messagingSenderId': "828869010735",
  'appId': "1:828869010735:web:7d3a681abf39dc7b7eadda",
  'measurementId': "G-N6V4SBKBLJ",
  'databaseURL':'https://yoyo2-ac013-default-rtdb.europe-west1.firebasedatabase.app/'
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

@app.route('/' ,methods = ['GET','POST'])
def signup():
    error = ('sorry you didnt succeed')
    if request.method == "POST":
       email = request.form["email"]
       password = request.form["password"]
       age = request.form["age"]
       global fullname
       fullname = request.form["fullname"]
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            UID = login_session['user']['localId']
            user = {'email':email,'fullname':fullname,'age':age}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('signin'))
       except Exception as e:
        print("SIGN UP ERROR:", e)
    return render_template('signup.html')

@app.route('/signin',methods = ["GET",'POST'])
def signin():
    error = "sorry you didnt succeed"
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('home'))
        except Exception as e:
            print("ERROR IN SIGN IN:", e)
            print(error)
            return render_template('signin.html')
    return render_template('signin.html')

@app.route('/home',methods = ['GET','POST'])
def home():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template('home.html',name = user['fullname'] )  
@app.route('/brtec')
def brtec():
    return render_template('brtec.html')
@app.route('/vdanx')
def vdanx():
    return render_template('vdanx.html')
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)