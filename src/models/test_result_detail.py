from src.utils.db import db 

class TestResultDetail(db.Model):
    __tablename__ = 'test_result_detail'
    id = db.Column(db.Integer, primary_key=True)
    test_result_id = db.Column(db.Integer, unique=True, nullable=False)
    question_id = db.Column(db.Integer, unique=True, nullable=False)
    answer = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.String(120), unique=True, nullable=False)
    updated_at = db.Column(db.String(120), unique=True, nullable=False)
    
    @staticmethod
    def get_all():
        return TestResultDetail.query.order_by(TestResultDetail.id).all()
    def __repr__(self):
        return '<id {}>'.format(self.id)
    # create function that needed by controllers
    @staticmethod
    def get_all_by_test_result_id(test_result_id):
        return TestResultDetail.query.filter_by(test_result_id=test_result_id).all()
    @staticmethod
    def get_all_by_question_id(question_id):
        return TestResultDetail.query.filter_by(question_id=question_id).all()
    @staticmethod
    def get_by_id(id):
        return TestResultDetail.query.filter_by(id=id).first()