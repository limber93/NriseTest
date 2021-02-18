from app.extention import restplus_api

user_ns = restplus_api.namespace('user', description='USER API')
session_ns = restplus_api.namespace('session', description='SESSION API')

# add api
from app.api import user
from app.api import session