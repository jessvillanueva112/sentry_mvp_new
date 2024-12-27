from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/api/students', methods=['GET'])
def get_students():
    # Example response
    return jsonify({"students": []}) 