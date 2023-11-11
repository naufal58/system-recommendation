from src.utils.db import db

class TestResult(db.Model):
    __tablename__ = 'test_result'
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