from src.pipeline.recommendation import system_recommendation_pipeline
from src.pipeline.preprocess_data import preprocess_pipeline
from src.pipeline.extract_features import extract_from_file
from src.pipeline.discretize import start
from src.pipeline.recommendation import generate_recommendation
from src.controllers.recommendation import Recommendation



# preprocess_pipeline('naufal', full_pipeline=False)
# extract_from_file('naufal', full_pipeline=False)
# start('naufal', training_data=False,  full_pipeline=False)
# result = Recommendation('aththar').generate_association_rules()
# Recommendation('aththar').generate_recommendation(result)

system_recommendation_pipeline('naufal')