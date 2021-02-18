from flask import Flask
from app.extention import restplus_api, orm_db
from app.api import user_ns, session_ns

def create_app(config_path=None):
    flask_app = Flask(__name__)
    if config_path:
        flask_app.config.from_object(config_path)
    register_extensions(flask_app)
    return flask_app


def register_extensions(app):
    # Initialize ORM
    orm_db.init_app(app)
    orm_db.app = app
    orm_db.create_all()


    restplus_api.init_app(app)

    # api
    restplus_api.add_namespace(user_ns)
    restplus_api.add_namespace(session_ns)