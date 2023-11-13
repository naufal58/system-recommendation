from src.utils.db import db

class TestResult(db.Model):
    __tablename__ = 'test_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    test_code = db.Column(db.String(120), unique=True, nullable=False)
    score = db.Column(db.String(120), unique=True, nullable=False)
    role_as = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.String(120), unique=True, nullable=False)
    updated_at = db.Column(db.String(120), unique=True, nullable=False)
    
    @staticmethod
    def get_all():
        return TestResult.query.order_by(TestResult.id).all()
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    # create function that needed by controller
    @staticmethod
    def get_all_by_user_id(user_id):
        return TestResult.query.filter_by(user_id=user_id).all()
    @staticmethod
    def get_by_id(id):
        return TestResult.query.filter_by(id=id).first()
    @staticmethod
    def get_by_test_code(test_code):
        return TestResult.query.filter_by(test_code=test_code).first()
    @staticmethod
    def get_by_user_id_and_test_code(user_id, test_code):
        return TestResult.query.filter_by(user_id=user_id, test_code=test_code).first()
    @staticmethod
    def get_by_user_id_and_name(user_id, name):
        return TestResult.query.filter_by(user_id=user_id, name=name).first()