import os

class Config:
    SECRET_KEY = "dev-secret"
    JWT_SECRET_KEY = "dev-jwt-secret"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:admin1234@localhost/desercion_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False