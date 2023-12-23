from src.controllers.recommendation import Recommendation
from src.pipeline.preprocess_data import preprocess_pipeline
from src.pipeline.extract_features import full_extraction_pipeline
from src.pipeline.discretize import start
import pandas as pd

def generate_recommendation(filename, to_excel=False, to_txt=False):
    rules = Recommendation(filename).generate_association_rules()
    recommendation = Recommendation(filename).generate_recommendation(rules)
    
    if recommendation and isinstance(recommendation, list):
        result = list(set(recommendation))
    else:
        result = str(recommendation)

    if to_txt:
        with open(f"Result.txt", 'w') as file:
            if isinstance(result, list):
                for item in result:
                    file.write(f"{item}\n")
            else:
                file.write(result)


def system_recommendation_pipeline(filename):
    print('Preprocessing data...')
    preprocess = preprocess_pipeline(filename, full_pipeline=True)

    print('Extracting features...')
    extracted_features = full_extraction_pipeline(preprocess)

    print('Discretizing data features...')
    discretize_data = start(training_data=extracted_features, filename=filename, full_pipeline=True)

    print('Association rules:')
    recommendation = generate_recommendation(filename, to_txt=True)

    return recommendation
