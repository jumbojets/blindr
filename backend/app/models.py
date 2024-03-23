from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy 'db' object without an app
db = SQLAlchemy()

class PermanentStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    constraints_hash = db.Column(db.String(128), unique=True, nullable=False)
    private_key = db.Column(db.String(2048), nullable=False)
    public_key = db.Column(db.String(2048), nullable=False)

class TemporaryStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    constraints_hash = db.Column(db.String(128), unique=True, nullable=False)
    private_value = db.Column(db.String(2048), nullable=False)
    public_value = db.Column(db.String(2048), nullable=False)