from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_tables():
    from Model import user, enterprise
    db.create_all()
