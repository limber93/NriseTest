import uuid
import datetime

from flask import request, jsonify
from flask_restplus import Resource
from marshmallow import Schema, fields
import bcrypt
from app.api import user_ns

from app.utils.required_params import required_params
from app.handler.user import UserHandler
from app.handler.session import SessionHandler



class UserCreateApiSchema(Schema):

    user_id = fields.Str(required=True)
    password = fields.Str(required=True)

@user_ns.route('')
class CreateUser(Resource):
    @required_params(UserCreateApiSchema())
    def post(self):
        try:
            user_handler = UserHandler()

            params = dict()

            params['user_id'] = request.get_json().get('user_id')
            params['password'] = bcrypt.hashpw(request.get_json().get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user_info = user_handler.read_filter(filter_col={'user_id': params['user_id'], 'deleted': False})
            # 중복 체크
            if user_info is not None:
                return {'message': 'exists Account'}, 409
            else:
                params['user_uuid'] = str(uuid.uuid4())
                user_handler.create(params)
        except Exception as e:
            return {'message': 'fail'}, 500
        else:
            return {'message': 'create user success', 'data': {'user_uuid': params['user_uuid']}}, 200


class UserDeleteApiSchema(Schema):

    session_id = fields.Str(required=True)


@user_ns.route('')
class DeleteUser(Resource):
    @required_params(UserDeleteApiSchema())
    def delete(self):
        try:
            session_handler = SessionHandler()
            user_handler = UserHandler()

            session_id = request.get_json().get('session_id')

            session_info = session_handler.read_filter(filter_col={'session_id': session_id})

            if session_info is not None:
                if session_info.logout_time is None:
                    if session_info.relation_user.deleted is False:
                        date = datetime.datetime.now()
                        # 세션 로그아웃 처리
                        session_handler.update(session_id, date)
                        user_handler.update_user_status(session_info.relation_user.user_id, date)
                    else:
                        return {'message': 'already deleted'}, 409
                else:
                    return {'message': 'session expired'}, 401
            else:
                return {'message': 'not exists session'}, 404

        except Exception as e:
            return {'message': 'fail'}, 500
        else:
            return {'message': 'delete user success'}, 200


@user_ns.route('/<user_uuid>')
class GetUser(Resource):
    def get(self, user_uuid):

        try:
            session_handler = SessionHandler()
            user_handler = UserHandler()

            session_list = list()
            result = dict()

            session_info = session_handler.read_all_filter(filter_col={'user_uuid': user_uuid})
            user_info = user_handler.read_filter(filter_col={'id': user_uuid})

            if user_info is None:
                return {'message': 'not exists account'}, 404
            else:
                for row in session_info:
                    s_dict = dict()
                    s_dict['session_id'] = row.session_id
                    s_dict['create_time'] = str(row.create_time.strftime("%Y-%m-%d-%H:%M:%S"))
                    s_dict['logout_time'] = None if row.logout_time is None else str(row.logout_time.strftime("%Y-%m-%d-%H:%M:%S"))
                    session_list.append(s_dict)

                result['session_list'] = session_list

                result['user_info'] = dict()

                result['user_info']['user_uuid'] = user_info.id
                result['user_info']['user_id'] = user_info.user_id
                result['user_info']['create_time'] = str(user_info.create_time.strftime("%Y-%m-%d-%H:%M:%S"))
                if user_info.deleted is True:
                    result['user_info']['deleted_time'] = str(user_info.deleted_time.strftime("%Y-%m-%d-%H:%M:%S"))

        except Exception as e:
            return {'message': 'fail'}, 500
        else:
            return {'message': 'success', 'data': result}, 200


