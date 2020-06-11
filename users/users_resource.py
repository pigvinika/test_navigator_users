import json

from users.users_model import UserData
from flask import request, make_response, jsonify
from flask_api.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from flask_restful import fields, marshal, Resource

user_fields = {'id': fields.Integer,
               'name': fields.String}

user_list_fields = {'count': fields.Integer,
                    'users': fields.List(fields.Nested(user_fields))}


class UserAddResource(Resource):
    @staticmethod
    def post(user_name):
        try:
            json.loads(request.data.decode("utf-8"))['name']
        except:
            return make_response(jsonify({'error': 'Invalid donation data'}), HTTP_400_BAD_REQUEST)

        UserData.create(user_name)


class UserListResource(Resource):
    @staticmethod
    def get():
        users = UserData.get_all()
        if not users:
            return make_response(jsonify({'error': 'The user database is empty'}), HTTP_404_NOT_FOUND)
        else:
            try:
                content = marshal({'count': len(users), 'users': [marshal(u, user_fields) for u in users]},
                                  user_list_fields)
            except:
                return make_response({'error': 'Corrupted database data'}, HTTP_500_INTERNAL_SERVER_ERROR)

            return make_response(content, HTTP_200_OK)
