from flask import Blueprint

main = Blueprint('main', __name__)

# Define routes here
@main.route('/')
def index():
    return "Hello, World!" 