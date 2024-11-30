from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#Customer
class User(db.Model):
	_tablename_="user"
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String,unique=True,nullable=False)
	password=db.Column(db.String,nullable=False)
	role=db.Column(db.Integer,nullable=False, default=1)
	name=db.Column(db.String,nullable=False)
	address=db.Column(db.String,nullable=False)
	pin_code=db.Column(db.Integer,nullable=False)
	#relationship
	service_req=db.relationship("Service_Request",cascade="all,delete",backref="user",lazy=True)

#Service
class Service(db.Model):
	_tablename_="service"
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String,nullable=False)
	price=db.Column(db.Float,nullable=False,default=0.0)
	time_required=db.Column(db.Integer,default=0)
	description=db.Column(db.String,nullable=False)
	service_req=db.relationship("Service_Request",cascade="all,delete",backref="service",lazy=True)
	




#Service_Professional
class Professional(db.Model):
	_tablename_="professional"
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
	service_req=db.relationship("Service_Request",cascade="all,delete",backref="professional",lazy=True)

#Service_Request
class Service_Request(db.Model):
	_tablename_="service_request"
	id=db.Column(db.Integer,primary_key=True)
	service_name=db.Column(db.String,nullable=False)
	service_id=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
	customer_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
	professional_id=db.Column(db.Integer,db.ForeignKey("professional.id"),nullable=False)
	dor=db.Column(db.DateTime,nullable=False)
	doc=db.Column(db.DateTime,nullable=False)
	status=db.Column(db.String,nullable=False)
	additional_request=db.Column(db.String,nullable=False)
	feedback=db.Column(db.String,nullable=False)

