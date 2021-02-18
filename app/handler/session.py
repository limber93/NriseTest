from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from app.extention import orm_db as db
from app.model.session import SessionModel


class SessionHandler:

    def __init__(self):
        self.session = db.session
        self.model = SessionModel

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

    def update(self, session_id, logout_date):
        result = True

        query_result = self.read_filter(filter_col={'session_id': session_id})

        query_result.logout_time = logout_date

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

    def read_all_filter(self, filter_col):
        return self.model.query.filter_by(**filter_col).order_by(desc(self.model.create_time)).all()
