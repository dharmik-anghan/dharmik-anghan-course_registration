import os 

class Config:
    SECRET_KEY=os.environ["SECRET_KEY"]
    DB_NAME=os.environ["DB_NAME"]
    DB_USER=os.environ["DB_USER"]
    DB_PASSWORD=os.environ["DB_PASSWORD"]
    DB_HOST=os.environ["DB_HOST"]
    DB_PORT=os.environ["DB_PORT"]
    EMAIL_USER=os.environ["EMAIL_USER"]
    EMAIL_PASS=os.environ["EMAIL_PASS"]
    EMAIL_FROM=os.environ["EMAIL_FROM"]
    JWT_ACCESS_TOKEN_LIFETIME=os.environ["JWT_ACCESS_TOKEN_LIFETIME"]
    JWT_REFRESH_TOKEN_LIFETIME=os.environ["JWT_REFRESH_TOKEN_LIFETIME"]
    DJANGO_LOG_LEVEL=os.environ.get("DJANGO_LOG_LEVEL")