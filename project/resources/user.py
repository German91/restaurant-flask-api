from project.models import UserModel
from flask_restful import Resource, reqparse


class UserList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='The username is required')
    parser.add_argument('password', type=str, required=True, help='The password is required')

    def get(self):
        users = UserModel.query.all() or None
        if users:
            return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}, 200
        return {'message': 'Users not found'}, 404

    def post(self):
        data = UserList.parser.parse_args()

        if UserModel.get_by_username(data['username']):
            return {'message': 'Username already exists'}, 400

        user = UserModel(data['username'], data['password'])

        try:
            user.save()
        except:
            return {'message': 'A problem occured creating account'}, 500

        return {'message': 'Account successfully created', 'user': user.json()}, 202


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='The username is required')

    def get(self, username):
        user = UserModel.get_by_username(username)

        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def put(self, username):
        data = User.parser.parse_args()

        user = UserModel.get_by_username(username)

        if user:
            user.username = data['username']

            user.save()
            return {'message': 'Account successfully updated', 'user': user.json()}, 200
        else:
            return {'message': 'User not found'}, 404

    def delete(self, username):
        user = UserModel.get_by_username(username)

        if user:
            user.delete()
            return {'message': 'Account successfully removed'}
        return {'message': 'User not found'}, 404