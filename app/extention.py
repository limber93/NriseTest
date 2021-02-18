from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy


restplus_api = Api(prefix='/api')
orm_db = SQLAlchemy()
