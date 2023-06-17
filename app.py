from flask import Flask, request, url_for, redirect, render_template, session
import pickle
import numpy as np
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_mail import Mail,Message
from random import randint
# from flask_ngrok import run_with_ngrok
import re

import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__, template_folder="templates")
# run_with_ngrok(app)
mail=Mail(app)
classifier = pickle.load(open("model.pkl", "rb"))
# Model saved with Keras model.save()


app.secret_key = 'xyzsdfg'
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='************' #your mail from which you are going to send otp
app.config['MAIL_PASSWORD']='*************'   #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
  
mysql = MySQL(app)

@app.route("/")
def index():
     return render_template("index.html")


@app.route("/about.html")
def about():
     return render_template("about.html")

@app.route("/help.html")
def help():
    return render_template("help.html")

# @app.route("/login")
# def login():
#     return render_template("login.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('dashboard.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/logout.html')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect('login.html')

  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
          
            msg=Message(subject='OTP',sender='aishbirambole@gmail.com',recipients=[email])
            msg.body=str(otp)
            mail.send(msg)
            
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            return render_template('verify.html')
            
            
            # mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    if otp==int(user_otp):

        # return "<h3>Email varification succesfull</h3>"  
        return render_template('dashboard.html') 
    return "<h3>Please Try Again</h3>"
    


@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")

@app.route("/disindex.html")
def disindex():
    return render_template("disindex.html")

@app.route("/choose.html")
def choose():
    return render_template("choose.html")
@app.route("/test.html")
def test():
    return render_template("test.html")











@app.route("/predict", methods=["POST"])
def home():
    d2 = float(request.form["ZZ"])
    d3 = float(request.form["c"])
    d4 = float(request.form["d"])
    d5 = float(request.form["e"])
    d6 = float(request.form["f"])
    d7 = float(request.form["g"])
    d8 = float(request.form["h"])
    d9 = float(request.form["i"])
    d10 = float(request.form["j"])
    d11 = float(request.form["k"])
    d12 = float(request.form["l"])
    d13 = float(request.form["m"])
    d14 = float(request.form["n"])
    d15 = float(request.form["o"])
    d16 = float(request.form["p"])
    d17 = float(request.form["q"])
    d18 = float(request.form["r"])
    d19 = float(request.form["s"])
    d20 = float(request.form["t"])
    d21 = float(request.form["u"])
    d22 = float(request.form["v"])
    # d23 = float(request.form["w"])
    d24 = float(request.form["x"])
    d25 = float(request.form["y"])
    d26 = float(request.form["z"])
    d27 = float(request.form["za"])
    d28 = float(request.form["zb"])
    d29 = float(request.form["zc"])

    arr = np.array(
        [
            [
                d2,
                d3,
                d4,
                d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16,
                d17, d18, d19, d20, d21, d22, d24, d25, d26, d27, d28, d29

            ]
        ]
    )
    pred = classifier.predict(arr)
    print(pred)
    return render_template("predict.html", data=pred)
@app.route("/remedies.html")
def hello_1():
    return render_template("remedies.html")

model =tf.keras.models.load_model('model.h5',compile=False)
def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(224, 224))
    show_img = image.load_img(img_path, grayscale=False, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    return preds





@app.route("/indexx.html")
def indexx():
    return render_template('indexx.html')
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        # x = x.reshape([64, 64]);
        disease_class = ['infected', 'notinfected']
        a = preds[0]
        ind=np.argmax(a)
        print('Prediction:', disease_class[ind])
        result=disease_class[ind]
        return result
    return None


@app.route("/test2.html")
def testt():
    return render_template("test2.html")


reg = pickle.load(open("model1.pkl", "rb"))


@app.route("/predictt", methods=["POST"])
def hom():
    d30 = float(request.form["ZZ"])
    d31 = float(request.form["AA"])
    d32 = float(request.form["BB"])
    d33 = float(request.form["CC"])
    d34 = float(request.form["DD"])
    d35 = float(request.form["EE"])
    d36 = float(request.form["FF"])
    d37 = float(request.form["GG"])
    d38 = float(request.form["HH"])
    d39 = float(request.form["II"])
    d40 = float(request.form["JJ"])
    d41 = float(request.form["KK"])
    d42 = float(request.form["LL"])
    d43 = float(request.form["MM"])
    d44 = float(request.form["NN"])

    arr = np.array(
        [
            [
                d30, d31, d32, d33, d34, d35, d36, d37, d38, d39, d40, d41, d42, d43, d44
            ]
        ]
    )

    pred1 = reg.predict(arr)
    print(pred1)
    return render_template("stage2.html", data=pred1)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
