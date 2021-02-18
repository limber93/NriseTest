import datetime
from app.extention import orm_db as db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(50))
    password = db.Column(db.String(60), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_logout_time = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean(), default=False)
    deleted_time = db.Column(db.DateTime)

    def __init__(self, params):
        self.id = params['user_uuid']
        self.user_id = params['user_id']
        self.password = params['password']