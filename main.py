from flask import Flask, flash, render_template, url_for, request, redirect, session
from pymongo import MongoClient
from bson.json_util import dumps
from random import randint

# POLI CHANGE THING TO UR THING, NO FORGET PLS
client = MongoClient("mongodb+srv://admin:admin@cluster0.oqvmr3o.mongodb.net/?retryWrites=true&w=majority")

db = client.Preject
users_db = db.users

db = client.Preject
vehicles_db = db.vehicles

app = Flask(__name__)
app.secret_key = "hkIbg#45f1_"



@app.route('/')
def home():
    return render_template('home.html')

#log in function
@app.route('/auth/login', methods=["GET","POST"])
def login():
    if "auth" in session:
        return render_template("home.html")
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            a = users_db.find_one({"username":username})
            b = users_db.find_one({"username":username},{"password":password})

            if a != None or b != None:
                a = a['username']
                b = b['password']

            if a != 'admin' or b != 'adminpassword':
                return render_template("login.html")

            session["auth"] = username

            return redirect(url_for("home"))

        else:
            return render_template("login.html")


#Adds items
@app.route('/create', methods=["GET","POST"])
def panel():
    if "auth" in session:
        if session["auth"] == "admin":
            session["auth"] = 'admin'
            if request.method == 'POST':
                id_ = randint(100,10000000)

                name = request.form['name']
                surname = request.form['surname']
                numberplate = request.form['numberplate']


                a = vehicles_db.find_one({"surname":surname})

                if a != None:
                    a = a['surname']
            
                if a == surname:
                    return render_template("create.html")
            
                session["auth"] = "admin"

                if name == "" or surname == "" or numberplate == "" :
                    return render_template('create.html')
                else:
                    vehicles_db.insert_one({"id":id_,"name":name,"surname":surname,"numberplate":numberplate})
                    return render_template('create.html')
            else:
                return render_template('create.html') 
        else:
            return render_template('home.html')

#Shows list
@app.route('/showvehiclelist')
def phones():
    return render_template('vehiclelist.html')  

#Deletes thing       
@app.route("/create/delete/<int:id_>", methods=["GET","POST"])
def delete(id_):
    if "auth" in session:
        if session["auth"] == "admin":
            vehicles_db.delete_one({"id":id_})
            return redirect(url_for("phones"))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


#logs out
@app.route('/logout', methods=["GET","POST"])
def logout():
    session.pop("auth", None)
    return redirect(url_for("home"))

#Shows things
@app.route('/data')
def data():
    vehicles = vehicles_db.find()
    data = list(vehicles)
    return dumps(data)




app.run(host='0.0.0.0', port=80, debug=True)