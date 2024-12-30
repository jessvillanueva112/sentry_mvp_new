from flask import Blueprint

# Import blueprints
from .main_blueprint import main as main_blueprint

# Function to register blueprints
def register_blueprints(app):
    app.register_blueprint(main_blueprint) 