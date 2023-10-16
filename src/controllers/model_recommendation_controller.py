# model_recommendation_controller.py
from flask import Blueprint
from mlxtend.frequent_patterns import fpgrowth
import pandas as pd

model_recommendation_controller = Blueprint('model_recommendation_controller', __name__)

@model_recommendation_controller.route('/recommendation')
def system_recommendation():
    data = pd.read_csv()
    df = pd.DataFrame(data)

    # Convert the dataset into a binary format (0s and 1s)
    df_encoded = pd.get_dummies(df.drop('TransactionID', axis=1))

    # Apply FP-growth to find frequent itemsets
    frequent_itemsets = fpgrowth(df_encoded, min_support=0.1, use_colnames=True)

    # Print all frequent itemsets and their support
    for index, row in frequent_itemsets.iterrows():
        print("Frequent Itemset:", list(row['itemsets']))
        print("Support:", row['support'])
        print()

    return 'ini adalah rekomendasi sistem!'
