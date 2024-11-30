
from flask import Flask,render_template,request
from flask import current_app as app
from .models import *


#app routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("username")
        pwd=request.form.get("password")
        usr=User.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0:
            return render_template("admin_page.html")
        if usr and usr.role==1:
            return render_template("cust_dashboard.html")

    return render_template("login.html")


@app.route("/cust_signup",methods=["GET","POST"])
def cust_signup():
    if request.method=="POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        name=request.form.get("name")
        address=request.form.get("address")
        pin_code=request.form.get("pincode") 
        new_usr=User(email=uname,password=pwd,name=name,address=address,pin_code=pin_code)   
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html")
    return render_template("cust_signup.html")

@app.route("/prof_signup",methods=["GET","POST"])
def prof_signup():
    if request.method=="POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        name=request.form.get("name")
        service=request.form.get("service")
        experience=request.form.get("experience")
        address=request.form.get("address")
        pin_code=request.form.get("pin_code") 
        new_prof=Professional(email=uname,password=pwd,name=name,service=service,experience=experience,address=address,pin_code=pin_code)   
        db.session.add(new_prof)
        db.session.commit()
        return render_template("login.html")
    return render_template("professional_signup.html")