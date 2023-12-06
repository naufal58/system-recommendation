from src.controllers.recommendation import Recommendation

def generate_recommendation(filename):
    result = Recommendation(filename).generate_association_rules()
    return result