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