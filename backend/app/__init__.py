import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Import and register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Initialize extensions
    db = SQLAlchemy()
    migrate = Migrate()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)

    return app 