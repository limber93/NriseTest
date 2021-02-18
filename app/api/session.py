import uuid
import datetime
from flask import request, current_app
from flask_restplus import Resource
from marshmallow import Schema, fields
import bcrypt
from app.api import session_ns

from app.utils.required_params import required_params
from app.handler.user import UserHandler
from app.handler.session import SessionHandler


class SessionPutApiSchema(Schema):

    user_id = fields.Str(required=True)
    password = fields.Str(required=True)

class SessionDeleteApiSchema(Schema):

    session_id = fields.Str(required=True)


@session_ns.route('')
class Session(Resource):
    @required_params(SessionPutApiSchema())
    def put(self):
        '''
        login
        '''
        try:
            session_handler = SessionHandler()
            user_handler = UserHandler()

            params = dict()

            user_id = request.get_json().get('user_id')
            password = request.get_json().get('password')

            user_info = user_handler.read_filter(filter_col={'user_id': user_id, 'deleted': False})

            if user_info is not None:
                if bcrypt.checkpw(password.encode('utf-8'), user_info.password.encode('utf-8')):
                    session_info = session_handler.read_filter(filter_col={'user_uuid': user_info.id, 'logout_time': None})
                    if session_info is not None:
                        return {'message': 'already auth'}, 409

                    params['user_uuid'] = user_info.id
                    params['ip_address'] = request.remote_addr
                    params['session_id'] = str(uuid.uuid4())
                    session_handler.create(params)
                else:
                    return {'message': 'incorrect password'}, 401
            else:
                return {'message': 'not exists account'}, 404

        except Exception as e:
            return {'message': 'fail'}, 500
        else:
            return {'message': 'login success', 'data': {"session_id": params['session_id']}}, 200

    @required_params(SessionDeleteApiSchema())
    def delete(self):
        '''
        logout
        '''

        try:
            session_handler = SessionHandler()
            user_handler = UserHandler()

            session_id = request.get_json().get('session_id')

            session_info = session_handler.read_filter(filter_col={'session_id': session_id, 'logout_time': None})

            if session_info is not None:
                logout_date = datetime.datetime.now()
                # 세션 로그아웃 처리
                session_handler.update(session_id, logout_date)
                # 유저 로그아웃 처리
                user_handler.update_logout(session_info.relation_user.user_id, logout_date)
            else:
                return {'message': 'session expired'}, 401

        except Exception as e:
            return {'message': 'fail'}, 500
        else:
            return {'message': 'logout success'}, 200





