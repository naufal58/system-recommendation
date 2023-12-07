from src.controllers.recommendation import Recommendation
from src.pipeline.preprocess_data import preprocess_pipeline
from src.pipeline.extract_features import full_extraction_pipeline
from src.pipeline.discretize import start

def generate_recommendation(filename, to_excel=False):
    result = Recommendation(filename).generate_association_rules()
    if to_excel:
        result.to_excel("result.xlsx", index=False)
    return result

def system_recommendation_pipeline(filename):
    print('Preprocessing data...')
    preprocess = preprocess_pipeline(filename, full_pipeline=True)

    print('Extracting features...')
    extracted_features = full_extraction_pipeline(preprocess)

    print('Discretizing data features...')
    discretize_data = start(training_data=extracted_features, filename=filename, full_pipeline=True)

    print('Association rules:')
    recommendation = generate_recommendation(filename, to_excel=True)

    return recommendation
