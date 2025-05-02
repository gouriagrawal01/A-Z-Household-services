
from flask import Flask,render_template,flash,flash,request,url_for,redirect,url_for,redirect
from flask import current_app as app
from .models import *
from datetime import datetime
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt

#app routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("username")
        pwd=request.form.get("password")
        hash_pwd=hash(pwd)
        usr=User.query.filter_by(email=uname,password=pwd).first()
        prof=Professional.query.filter_by(email=uname,password=pwd).first()
        
        
        if usr and usr.role==0: #Admin
            return redirect(url_for("admin_dashboard",name=uname))
        elif usr and usr.role==1: #Customer
            return redirect(url_for("cust_dashboard",name=uname))
        elif prof : #professional
            if prof.is_approved=="Yes":
                return redirect(url_for("prof_dashboard",name=uname))
            else:
                return render_template("login.html",msg="Account not approved,wait for admin approval")
        else:
            return render_template("login.html",msg="Invalid Credentials")
    return render_template("login.html",msg="")



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
        return render_template("login.html",msg="")
    return render_template("cust_signup.html")

@app.route("/prof_signup",methods=["GET","POST"])
def prof_signup():
    if request.method=="POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        name=request.form.get("name")
        service=request.form.get("service")
        experience=request.form.get("experience")
        file=request.files["file_upload"]
        url=""
        if file.filename:
            file_name=secure_filename(file.filename)
            url='./uploaded_files/'+name+"_"+file_name
            file.save(url)
        address=request.form.get("address")
        pin_code=request.form.get("pin_code")
        service_id=get_service_by_name(service)        
        new_prof=Professional(email=uname,password=pwd,name=name,service=service,service_id=service_id,resume_url=url,experience=experience,address=address,pin_code=pin_code)   
        db.session.add(new_prof)
        db.session.commit()
        return render_template("login.html",msg="Registration Successful,wait for admin approval")
    return render_template("professional_signup.html",msg="")


@app.route("/admin_dashboard/<name>")
def admin_dashboard(name):
    services=get_services()
    professionals=get_professionals()
    service_requests=get_requests()
    customers=get_customers()
    return render_template("admin_dashboard.html",name=name,services=services,professionals=professionals,service_requests=service_requests,customers=customers)

@app.route("/cust_dashboard/<name>")
def cust_dashboard(name):
    services=get_services()
    service_requests=get_requests()
    return render_template("cust_dashboard.html",name=name,services=services,service_requests=service_requests)

@app.route("/prof_dashboard/<name>")
def prof_dashboard(name):
    service_requests=get_requests()
    user=get_user_request(name) 
    return render_template("prof_dashboard.html",name=name,service_requests=service_requests)


@app.route("/service/<name>",methods=["GET","POST"])
def add_service(name):
    if request.method=="POST":
        service_name=request.form.get("service_name")
        price=request.form.get("price")
        time_required=request.form.get("time_required")
        description=request.form.get("description")
        new_service=Service(name=service_name,price=price,time_required=time_required,description=description)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("add_service.html",name=name)

@app.route("/search/<name>",methods=["GET","POST"])
def search(name):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        by_service=search_by_service(search_txt)
        by_professional=search_by_professional(search_txt)
        if by_service:
            return render_template("admin_dashboard.html",name=name,services=by_service)
        
        if by_professional:
            return render_template("admin_dashboard.html",name=name,professionals=by_professional)

    return redirect(url_for("admin_dashboard",name=name))

@app.route("/search_cust/<name>",methods=["GET","POST"])
def search_cust(name):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        option=request.form.get("option")
        if option=="name":
            by_name=search_by_service(search_txt)
            return render_template("cust_dashboard.html",name=name,services=by_name)
        elif option=="location":
            by_location=search_by_location(search_txt)
            return render_template("cust_dashboard.html",name=name,services=by_location)
        elif option=="pin_code":
            by_pin_code=search_by_pin_code(search_txt)
            return render_template("cust_dashboard.html",name=name,services=by_pin_code)
    return render_template("search_cust.html",name=name)
        

@app.route("/edit_service/<id>/<name>",methods=["GET","POST"])
def edit_service(id,name):
    v=get_service(id)
    if request.method=="POST":
        service_name=request.form.get("service_name")
        price=request.form.get("price")
        time_required=request.form.get("time_required")
        description=request.form.get("description")
        v.name=service_name
        v.price=price
        v.time_required=time_required
        v.description=description
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("edit_service.html",service=v,name=name)

@app.route("/delete_service/<id>/<name>",methods=["GET","POST"])
def delete_service(id,name):
    v=get_service(id)
    db.session.delete(v)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))

@app.route("/admin_approval/<id>/<name>",methods=["GET","POST"])
def admin_approval(id,name):
    p=get_professional_id(id)
    p.is_approved="Yes"
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))


@app.route("/delete_prof/<id>/<name>",methods=["GET","POST"])
def delete_prof(id,name):
    v=get_professional_id(id)
    db.session.delete(v)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))


@app.route("/accept_service/<id>/<name>",methods=["GET","POST"])
def accept_service(id,name):
    v=get_service_request(id)
    v.status="Accepted"
    db.session.commit()
    return redirect(url_for("prof_dashboard",name=name))

@app.route("/reject_request/<id>/<name>",methods=["GET","POST"])
def reject_request(id,name):
    v=get_service_request(id)
    v.status="Rejected"
    db.session.commit()
    return redirect(url_for("prof_dashboard",name=name))

@app.route("/close_request/<id>/<name>",methods=["GET","POST"])
def close_request(id,name):
    v=get_service_request(id)
    v.status="Closed"
    v.doc=datetime.now()
    db.session.commit()
    return redirect(url_for("prof_dashboard",name=name))

@app.route("/close_request_cust/<id>/<name>",methods=["GET","POST"])
def close_request_cust(id,name):
    v=get_service_request(id)
    p_id=v.professional_id
    p=get_professional(p_id)
    if request.method=="POST":
        doc=request.form.get("dor")
        feedback=request.form.get("feedback")
        rating=request.form.get("rating")
        v.status="Closed"
        v.doc=doc
        v.feedback=feedback
        p.rating=Professional.query.with_entities(func.avg(Professional.rating))
        db.session.commit()
        return redirect(url_for("cust_dashboard",name=name))
    return render_template("close_request_cust.html",service_request=v,name=name)

    

@app.route("/request_service/<service_id>/<name>",methods=["GET","POST"])
def request_service(service_id,name):
    service=get_service(service_id)
    user=get_user(name)
    professionals=get_professional(service_id)
    if request.method=="POST":
        service_name=service.name
        service_id=service.id
        customer_id=user.id
        professional_id=request.form.get("professional")
        dor=request.form.get("dor")
        d_or=datetime.fromisoformat(dor) 
        new_request=Service_Request(service_name=service_name,service_id=service_id,customer_id=customer_id,professional_id=professional_id,dor=d_or)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for("cust_dashboard",name=name))
    return render_template("request_service.html",name=name,professionals=professionals,service=service)

@app.route("/admin_summary")
def admin_summary():
    plot=get_service_request_summary()
    plot.savefig("./static/images/service_request_summary.jpeg")
    plot.clf()
    plot2=get_professional_rating()
    plot2.savefig("./static/images/professiona_rating_summary.jpeg")
    return render_template("admin_summary.html")



@app.route("/edit_request/<id>/<name>",methods=["GET","POST"])
def edit_request(id,name):
    v=get_service_request(id)
    if request.method=="POST":
        dor=request.form.get("dor")
        status=request.form.get("status")
        additional_request=request.form.get("additional_request")
        feedback=request.form.get("feedback")
        v.dor=dor
        v.status=status
        v.additional_request=additional_request
        v.feedback=feedback
        db.session.commit()
        return redirect(url_for("cust_dashboard",name=name))
    return render_template("edit_request.html",service_request=v,name=name)


def get_service(id):
    services=Service.query.filter_by(id=id).first()
    return services

def get_service_by_name(name):
    services=Service.query.filter_by(name=name).first()
    return services.id

def get_service_request(id):
    service_requests=Service_Request.query.filter_by(id=id).first()
    return service_requests

def get_user(name):
    user=User.query.filter_by(email=name).first()
    return user

def get_user_request(id):
    user=User.query.filter_by(id=id).first()
    return user

def get_professional_id(id):
    professional=Professional.query.filter_by(id=id).first()
    return professional

def get_professional(id):
    professionals=Professional.query.filter_by(service_id=id).all()
    return professionals

def search_by_service(search_txt):
    services=Service.query.filter(Service.name.ilike(f"%{search_txt}%")).all()
    return services

def search_by_professional(search_txt):
    professionals=Professional.query.filter(Professional.name.ilike(f"%{search_txt}%")).all()
    return professionals

def search_by_location(search_txt):
    services=Service.query.filter(Service.address.ilike(f"%{search_txt}%")).all()
    return services

def search_by_pin_code(search_txt):
    services=Service.query.filter(Service.pin_code.ilike(f"%{search_txt}%")).all()
    return services

def get_services():
    services=Service.query.all()
    return services

def get_professionals():
    professionals=Professional.query.all()
    return professionals

def get_requests():
    service_requests=Service_Request.query.all()
    return service_requests

def get_customers():
    customers=User.query.all()
    return customers

def get_service_request_summary():
    status_data = db.session.query(
        Service_Request.status, func.count(Service_Request.id)
    ).group_by(Service_Request.status).all()
    labels = [status for status, count in status_data]
    counts = [count for status, count in status_data]
    plt.bar(labels,counts,color='green',width=0.2)
    plt.title("Service Requests Status")
    plt.xlabel('Service Requests')
    plt.ylabel('Count')
    return plt

def get_professional_rating():
    ratings=Professional.query.all()
    summary={}
    for r in ratings:
        summary[r.id]=r.rating
    plt.bar(list(summary.keys()),list(summary.values()),color='blue',width=0.2)
    plt.title("Professionals Rating")
    plt.xlabel('Professional id')
    plt.ylabel('Rating')
    return plt
    
    