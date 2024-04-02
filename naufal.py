from src.controllers.data_preprocess import DataPreprocess, convert_to_json
from src.controllers.feature_extraction import FeatureExtraction
from src.controllers.recommendation import Recommendation
from src.pipeline.preprocess_data import preprocess_pipeline
from src.pipeline.extract_features import extract_from_file
from src.pipeline.recommendation import output_results
from src.pipeline.discretize import start
import pandas as pd

preprocessor = preprocess_pipeline('dimasSC')
feature_extraction =  extract_from_file('dimasSC')
ECLAT = output_results('dimasSC', to_excel=False, to_txt=True)
# print(preprocessor)
# # 1. relative_pronouns