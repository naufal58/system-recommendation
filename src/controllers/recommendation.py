from src.models.question_bank import QuestionBank;
from src.models.test_result import TestResult;
from src.models.test_result_detail import TestResultDetail;
from src.models.user import User;

# import render template
from flask import render_template

class Recommendation():
    def __init__(self, user):
        self.user = user
    def HelloWord():
        return "hello word"
    
    # get all question bank 
    @staticmethod
    def recommendation(self):
        # get user data from db 
        question_banks = QuestionBank.getAll()
        
        # create test result and detail for each question bank
        for question_bank in question_banks:
            test_result = TestResult.create(question_bank.id, self.user.id)
            test_result_details = TestResultDetail.create(test_result.id, question_bank.id)
            # calculate score
            total_score = 0
            correct_answer_count = 0
            for test_result_detail in test_result_details:
                total_score += test_result_detail.score
                if test_result_detail.score == 1:
                    correct_answer_count += 1
            # update score for test result
            test_result.update(total_score, correct_answer_count)
        # get test result
        test_results = TestResult.getByUserId(self.user.id)
        # get test result detail
        test_result_details = TestResultDetail.getByUserId(self.user.id)
        # get user
        user = User.getById(self.user.id)
        # calculate score
        total_score = 0
        correct_answer_count = 0
        for test_result_detail in test_result_details:
            total_score += test_result_detail.score
            if test_result_detail.score == 1:
                correct_answer_count += 1
        # update score for user
        user.update(total_score, correct_answer_count)
        # get all user
        users = User.getAll()
        # sort user by score
        users.sort(key=lambda x: x.total_score, reverse=True)
        # get user rank
        user_rank = 0
        for index, user in enumerate(users):
            if user.id == self.user.id:
                user_rank = index + 1
                break
        # get user rank percentage
        user_rank_percentage = 0
        if user_rank > 0:
            user_rank_percentage = (user_rank / len(users)) * 100
        # get user rank percentage

        # get user rank percentage
        user_rank_percentage = 0
        if user_rank > 0:
            user_rank_percentage = (user_rank / len(users)) * 100
        # get user rank percentage
        return render_template('dashboard/index.html', title='Dashboard', user=user, test_results=test_results
            , test_result_details=test_result_details, users=users, user_rank=user_rank
            , user_rank_percentage=user_rank_percentage)
    