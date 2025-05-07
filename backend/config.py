class Config():
    DEBUG=False
    SQLALCHEMY_TRACK_NOTIFICATIONS=True

class LocalDevelopmentConfig(Config):
    #configuration for database
    SQLALCHEMY_DATABASE_URI="sqlite:///household.sqlite3"
    DEBUG=True

    #configuration for security
    SECRET_KEY="a-secret-key" #hash user cred
    SECURITY_PASSWORD_HASH="bcrypt" #hashing password in db
    SECURITY_PASSWORD_SALT="a-password-salt" #helps in hashng the password
    WTF_CSRF_ENABLED=False 
    SECURTIY_TOKEN_AUTHENTICATION_HEADER="Authentication-Token" 

