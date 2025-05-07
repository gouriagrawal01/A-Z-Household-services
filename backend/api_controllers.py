from flask_restful import Resource,Api,reqparse
from flask import request
from flask_security import auth_required,roles_required,roles_accepted,current_user
from datetime import *
from .models import *

api=Api()

def roles_list(roles):
    roles_list=[]
    for role in roles:
        roles_list.append(role.name)
    return roles_list

class ShowApi(Resource):
    @auth_required('token')
    @roles_accepted('user','admin','professional')
    def get(self):
        service_requests=Service_Request.query.all()
        request_json=[]
        for r in service_requests:
            request_json.append({'id':r.id,'service_name':r.service_name,'service_id':r.service_id,'customer_id':r.customer_id,'professional_id':r.professional_id,'dor':str(r.dor),'doc':str(r.doc),'status':r.status,'additional_request':r.additional_request,'feedback':r.feedback})
        return request_json    

    @auth_required('token')
    @roles_required('user')
    def post(self):
        service_name=request.json.get('service_name')
        dor=request.json.get('dor')
        service_id=request.json.get('service_id')
        professional_id=request.json.get('professional_id')
        additional_request=request.json.get('additional_request')
        feedback=request.json.get('feedback')
        customer_id=request.json.get('customer_id')
        dor_date=datetime.strptime(dor,"%Y-%m-%d %H:%M:%S")
        new_request=Service_Request(service_name=service_name,dor=dor_date,service_id=service_id,professional_id=professional_id,additional_request=additional_request,feedback=feedback,customer_id=customer_id)        
        db.session.add(new_request)
        db.session.commit()
        return {
               "message":"Service Request created successfully"
         },400
    
    @auth_required('token')
    @roles_required('user')
    def put(self,service_id):
        service=Service_Request.query.get(service_id)
        if service:
            service.service_name=request.json.get('service_name')
            dor=request.json.get('dor')
            service.dor=datetime.strptime(dor,"%Y-%m-%d %H:%M:%S")
            service.service_id=request.json.get('service_id')
            service.professiona_id=request.json.get('professional_id')
            service.additional_request=request.json.get('additional_request')
            service.feedback=request.json.get('feedback')
            db.session.commit()
            return {
             "message":"Service Request updated successfully"},200
        return {
            "message":"Service Request id not found"
        },400
    
    @auth_required('token')
    @roles_required('user')
    def delete(self,service_id):
        service=Service_Request.query.get(service_id)
        if service:
            db.session.delete(service)
            db.session.commit()
            return {
                    "message":"Service Request deleted successfully"
            }
        else:
            return {
                    "message":"Service Request not found"
            },404

class Show_Request(Resource):
    @auth_required('token')
    @roles_accepted('user','admin','professional')
    def get(self,id):
        r=Service_Request.query.filter(id=id).first()
        if r:
            request_json=[]
            request_json.append({'id':r.id,'service_name':r.service_name,'service_id':r.service_id,'customer_id':r.customer_id,'professional_id':r.professional_id,'dor':str(r.dor),'doc':str(r.doc),'status':r.status,'additional_request':r.additional_request,'feedback':r.feedback})
            return request_json 
        return{
            "message":"No request found"
        },404
           


api.add_resource(ShowApi,"/api/get_requests","/api/create","/api/update/<int:service_id>","/api/delete/<int:service_id>")
api.add_resource(Show_Request,"/api/get_request")