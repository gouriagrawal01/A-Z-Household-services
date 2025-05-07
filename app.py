from flask import Flask
from backend.models import *
from backend.api_controllers import *
from backend.config import LocalDevelopmentConfig
from flask_security import Security,SQLAlchemyUserDatastore
from  flask_security import hash_password

app=None

def setup_app():
    app=Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    datastore=SQLAlchemyUserDatastore(db,User,Role)
    app.security=Security(app,datastore)
    app.app_context().push()
    return app


app=setup_app()


with app.app_context():
    db.create_all()

    app.security.datastore.find_or_create_role(name='admin',description='Superuser')
    app.security.datastore.find_or_create_role(name='professional',description='Service provider')
    app.security.datastore.find_or_create_role(name='user',description='user')
    db.session.commit()

    if not app.security.datastore.find_user(email = "user0@admin.com"):
        app.security.datastore.create_user(email = 'user0@admin.com',
                                           username = "admin1",
                                           password = hash_password('1234'),
                                           roles = ['admin'])
        
    if not app.security.datastore.find_user(email="user1@user.com"):
        app.security.datastore.create_user(email="user1@user.com",username="user",password=hash_password('1234'),roles=['user'])

    if not app.security.datastore.find_user(email="prof1@user.com"):
        app.security.datastore.create_user(email="prof1@user.com",username="prof1",password=hash_password('1234'),roles=['professional'])
        
    db.session.commit()


from backend.controllers import *

if __name__=="__main__":
    app.run()

