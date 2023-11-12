from src.utils.db import db 

class QuestionBank(db.Model):
    __tablename__ = 'question_banks'
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
    # create function that needed by controllers
    @staticmethod
    def get_by_id(id):
        return QuestionBank.query.filter_by(id=id).first()
    @staticmethod
    def get_by_question(question):
        return QuestionBank.query.filter_by(question=question).first()
    @staticmethod
    def get_by_answer(answer):
        return QuestionBank.query.filter_by(answer=answer).first()