from src.utils.db import db 

class QuestionBank(db.Model):
    __tablename__ = 'question_bank'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(120), unique=True, nullable=False)
    answer = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.String(120), unique=True, nullable=False)
    updated_at = db.Column(db.String(120), unique=True, nullable=False)
    
    @staticmethod
    def get_all():
        return QuestionBank.query.order_by(QuestionBank.id).all()
    def __repr__(self):
        return '<id {}>'.format(self.id)