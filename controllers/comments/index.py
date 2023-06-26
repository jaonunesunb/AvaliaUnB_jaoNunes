from flask import Blueprint, request, jsonify
from services.comments.index import create_comment ,edit_comment, get_comments, get_comment_by_id, delete_comment

comments_blueprint = Blueprint('comments', __name__)

@comments_blueprint.route('/comments', methods=['POST'])
def create_comments_controller():
    data = request.json
    create_comment(data['nome'], data['email'], data['senha'], data['matricula'], data['curso'])
    return jsonify('comments created successfully'), 201

@comments_blueprint.route('/comments/<int:comments_id>', methods=['PUT'])
def edit_comments_controller(comments_id):
    data = request.json
    edit_comment(comments_id, data['nome'], data['email'], data['senha'], data['curso'])
    return jsonify('comments updated successfully')

@comments_blueprint.route('/comments', methods=['GET'])
def get_comments_controller():
    comments = get_comments()
    return jsonify(comments)

@comments_blueprint.route('/comments/<int:comments_id>', methods=['GET'])
def get_comments_by_id_controller(comments_id):
    comments = get_comment_by_id(comments_id)
    return jsonify(comments)

@comments_blueprint.route('/comments/<int:comments_id>', methods=['DELETE'])
def delete_comments_controller(comments_id):
    delete_comment(comments_id)
    return jsonify({'message': 'comments deleted successfully'})
