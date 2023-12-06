from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
import pandas as pd
from src.utils.helper_functions import get_training_data

class Recommendation():
    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        data = get_training_data(self.filename)

        df = pd.DataFrame(data)

        df_discretized = pd.DataFrame()

        not_included = ['tense_type', 'key_is_homophone', 'answer_is_homophone', 'error_type']
        for column in df.columns:
            if column in not_included:
                df_discretized[column] = df[column]
                continue
            df_discretized[column+'_bins'] = pd.cut(df[column], bins=3, labels=['l_'+column, 'm_'+column, 'h_'+column])

        result_df = pd.concat([df, df_discretized], axis=1)

        return df_discretized

    def generate_association_rules(self):
        temp_data = self.get_data()
        data_list = []
        for data in temp_data.values.tolist():
            data = [value for value in data if type(value) == str and not value.startswith('l_')]
            data_list.append(data)

        encoder = TransactionEncoder()
        encoded_data = encoder.fit(data_list).transform(data_list)

        df = pd.DataFrame(encoded_data, columns=encoder.columns_)

        frequent_itemsets = fpgrowth(df, min_support=0.3, use_colnames=True)

        rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.7)

        return rules
