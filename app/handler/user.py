import datetime
from app.extention import orm_db as db
from app.model.user import UserModel

from sqlalchemy.exc import SQLAlchemyError

class UserHandler:

    def __init__(self):
        self.session = db.session
        self.model = UserModel

    def create(self, params):
        result = True
        try:
            self.session.add(self.model(params))
            self.session.commit()
        except SQLAlchemyError as db_e:
            self.session.rollback()
            raise db_e
        except Exception as e:
            self.session.rollback()
            raise e
        return result

    def update_user_status(self, user_id, update_date):
        result = True

        query_result = self.read_filter(filter_col={'user_id': user_id, 'deleted': False})

        query_result.deleted = True
        query_result.last_logout_time = update_date
        query_result.deleted_time = update_date

        try:
            self.session.commit()
        except SQLAlchemyError as db_e:
            self.session.rollback()
            raise db_e
        except Exception as e:
            self.session.rollback()
            raise e
        return result

    def update_logout(self, user_id, logout_date):
        result = True

        query_result = self.read_filter(filter_col={'user_id': user_id, 'deleted': False})

        query_result.last_logout_time = logout_date

        try:
            self.session.commit()
        except SQLAlchemyError as db_e:
            self.session.rollback()
            raise db_e
        except Exception as e:
            self.session.rollback()
            raise e
        return result

    def read_filter(self, filter_col):
        return self.model.query.filter_by(**filter_col).first()