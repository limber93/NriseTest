import datetime
from app.extention import orm_db as db
from sqlalchemy.orm import relationship

class SessionModel(db.Model):
    __tablename__ = 'session'

    session_id = db.Column(db.String(120), primary_key=True)
    user_uuid = db.Column(db.String(50), db.ForeignKey('users.id'))
    logout_time = db.Column(db.DateTime)
    ip_address = db.Column(db.String(15))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    relation_user = relationship('UserModel')

    def __init__(self, params):

        self.session_id = params['session_id']
        self.user_uuid = params['user_uuid']
        self.ip_address = params['ip_address']
        self.create_time = datetime.datetime.now()