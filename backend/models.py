from flask_security import UserMixin,RoleMixin
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

#Customer
class User(db.Model, UserMixin):
	__tablename__="user"
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String,unique=True,nullable=False)
	password=db.Column(db.String,nullable=False)
	role=db.Column(db.Integer,nullable=False, default=1)
	name=db.Column(db.String,nullable=False)
	address=db.Column(db.String,nullable=False)
	pin_code=db.Column(db.Integer,nullable=False)
	fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
	#relationship
	service_req=db.relationship("Service_Request",cascade="all,delete",backref="user",lazy=True)
	roles = db.relationship('Role', secondary='user_roles', backref='user')
#Service
class Service(db.Model):
	__tablename__="service"
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String,nullable=False)
	price=db.Column(db.Float,nullable=False,default=0.0)
	time_required=db.Column(db.Integer,default=0)
	description=db.Column(db.String,nullable=False)
	service_req=db.relationship("Service_Request",cascade="all,delete",backref="service",lazy=True)
	service_prof=db.relationship("Professional",cascade="all,delete",backref="services",lazy=True)




#Service_Professional
class Professional(db.Model):
	__tablename__="professional"
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String,unique=True,nullable=False)
	password=db.Column(db.String,nullable=False)
	role=db.Column(db.Integer,nullable=False, default=2)
	name=db.Column(db.String,nullable=False)
	service=db.Column(db.String,nullable=False)
	service_id=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
	experience=db.Column(db.Integer,nullable=False)
	address=db.Column(db.String,nullable=False)
	pin_code=db.Column(db.Integer,nullable=False)
	rating=db.Column(db.Float,default=0.0)
	resume_url=db.Column(db.String,nullable=False)
	is_approved=db.Column(db.String,default="No")
	service_req=db.relationship("Service_Request",cascade="all,delete",backref="professional",lazy=True)
	roles = db.relationship('Role', secondary='user_roles', backref='professional')

#Service_Request
class Service_Request(db.Model):
	__tablename__="service_request"
	id=db.Column(db.Integer,primary_key=True)
	service_name=db.Column(db.String,nullable=False)
	service_id=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
	customer_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
	professional_id=db.Column(db.Integer,db.ForeignKey("professional.id"),nullable=False)
	dor=db.Column(db.DateTime,nullable=False)
	doc=db.Column(db.DateTime)
	status=db.Column(db.String,default="Requested")
	additional_request=db.Column(db.String)
	feedback=db.Column(db.String)


