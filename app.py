from flask import Flask
from backend.models import db

app=None

def setup_app():
    app=Flask(__name__)    
    #sqlite connection
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household_services.db"#having db file
    db.init_app(app) #Flask connected to db
    app.app_context().push() #DIRECT ACCESS TO OTHER MODULES
    app.debug=True
    print("Household services is started....")


setup_app()

from backend.controllers import *

if __name__=="__main__":
    app.run()