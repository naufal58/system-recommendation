from src.controllers.recommendation import Recommendation
from src.pipeline.preprocess_data import preprocess_pipeline
from src.pipeline.extract_features import full_extraction_pipeline
from src.pipeline.discretize import start
import os
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

# def output_results(filename, to_excel=False, to_txt=False):
#     recommendation = Recommendation(filename)
#     rules = recommendation.find_frequent_itemsets(min_support = 0.1, min_confidence=0.1)
    
#     if to_excel:
#         excel_filename = "association_rules.xlsx"
#         rules.to_excel(excel_filename, index=False, engine='openpyxl')
#         print(f"Rules exported to {excel_filename}")

#     if to_txt:
#         txt_filename = "association_rules.txt"
#         with open(txt_filename, 'w') as file:
#             for index, row in rules.iterrows():
#                 # Write all items in the row, not just antecedents and consequents
#                 file.write(', '.join([f"{key}: {value}" for key, value in row.items()]) + '\n')
#         print(f"Rules exported to {txt_filename}")

def output_results(filename, to_excel=False, to_txt=False):
    recommendation = Recommendation(filename)
    rules_df = recommendation.find_frequent_itemsets(min_support=0.08, min_confidence=0.9)
    
    # Getting the competency percentages
    _, comp_percentage = recommendation.get_data()
    
    # Generate the numbered tiered recommendations
    tiered_recommendations = recommendation.generate_numbered_tiered_recommendations()
    
    # Print the tiered recommendations to view the results
    for rec in tiered_recommendations:
        print(rec)
    
    # Define the path for saving files
    save_path = os.path.join(os.getcwd(), 'Rekomendasi')
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # Create the directory if it does not exist
    
    # Export tiered recommendations and rules_df to Excel if requested
    if to_excel:
        excel_filename_recom = os.path.join(save_path, "tiered_rekomendasi.xlsx")
        excel_filename_rules = os.path.join(save_path, "rules_df.xlsx")
        
        try:
            # Convert the tiered_recommendations list to a DataFrame for Excel export
            df_to_export_recom = pd.DataFrame({'Recommendation': tiered_recommendations})
            df_to_export_recom.to_excel(excel_filename_recom, index=False)
            print(f"Tiered recommendations exported to {excel_filename_recom}")
            
            # Export rules_df to Excel
            rules_df.to_excel(excel_filename_rules, index=False)
            print(f"Rules DataFrame exported to {excel_filename_rules}")
        except Exception as e:  # Catching a more general exception
            print(f"Error exporting to Excel: {e}")
    
    # Export tiered recommendations and rules_df to text file if requested
    if to_txt:
        txt_filename_recom = os.path.join(save_path, "tiered_rekomendasi.txt")
        txt_filename_rules = os.path.join(save_path, "rules_df.txt")
        
        try:
            with open(txt_filename_recom, 'w') as file_recom:
                for rec in tiered_recommendations:
                    file_recom.write(str(rec) + "\n")
            print(f"Tiered recommendations exported to {txt_filename_recom}")
            
            with open(txt_filename_rules, 'w') as file_rules:
                for index, row in rules_df.iterrows():
                    file_rules.write(str(row.to_dict()) + "\n")
            print(f"Rules DataFrame exported to {txt_filename_rules}")
        except Exception as e:  # Catching a more general exception
            print(f"Error exporting to text file: {e}")

def system_recommendation_pipeline(filename):
    print('Preprocessing data...')
    preprocess = preprocess_pipeline(filename, full_pipeline=True)

    print('Extracting features...')
    extracted_features = full_extraction_pipeline(preprocess)

    # print('Discretizing data features...')
    # discretize_data = start(training_data=extracted_features, filename=filename, full_pipeline=True)

    print('Association rules:')
    recommendation = generate_recommendation(filename, to_txt=True)

    return recommendation
