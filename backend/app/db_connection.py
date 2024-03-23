from decouple import config
# from database import DB
from flask_sqlalchemy import SQLAlchemy
from models import PermanentStorage, TemporaryStorage, db


def create_db_url():
    # Load database configuration from the .env file
    db_config = {
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'port': config('DB_PORT'),
        'database': config('DB_NAME')
    }

    # Construct the database URL
    db_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    return db_url

    
def setup_db_connection(app):
    db_url = create_db_url()
    
    # Set the SQLAlchemy configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.db = db
    return app