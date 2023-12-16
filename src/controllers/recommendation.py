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
        
        rules = rules.sort_values(by=['support', 'lift'], ascending=[False, False])


        rules = rules[rules.apply(lambda row: len(row['antecedents']) + len(row['consequents']) <= 3, axis=1)]
        filtered_rules = rules.head(3)
        print(filtered_rules)
        
        return filtered_rules

    def generate_recommendation(self, filtered_rules):
        rules_list = filtered_rules.to_dict('records')
        print(rules_list)
        recommendation_sentence = []
        for rule in rules_list:
            antecedents = ', '.join(rule['antecedents'])
            consequents = ', '.join(rule['consequents'])

            action, slug = self.mapping_action(antecedents, consequents)

            recommendation = f"You must {action}. You can learn on our website at smartengtest/{slug}."
            recommendation_sentence.append(recommendation)
        print(recommendation_sentence)
            
        return recommendation_sentence
    
    def mapping_action (self, antecedent,consequent):
        actions = {
            'tenses types': ("learn more about modifier tenses", "past-tense"),
            'past': ("focus more on past tense usage including all the modifiers like past continuous, past future, and past present", "past-tense"),
            'present': ("concentrate on present tense structures", "present-tense"),
            'future': ("prepare for future tense scenarios", "future-tense"),
            'l_vocabulary_difficulty_score': ("enhance basic vocabulary skills", "vocabulary"),
            'm_vocabulary_difficulty_score': ("build on intermediate vocabulary", "vocabulary"),
            'h_vocabulary_difficulty_score': ("master advanced vocabulary", "vocabulary"),
            'l_conjuctions': ("practice basic conjunctions", "conjunctions"),
            'm_conjuctions': ("improve use of intermediate conjunctions", "conjunctions"),
            'h_conjuctions': ("refine usage of complex conjunctions", "conjunctions"),
            'l_flesch_reading_ease': ("read simpler texts to improve comprehension", "reading-materials"),
            'm_flesch_reading_ease': ("engage with moderately complex texts", "reading-materials"),
            'h_flesch_reading_ease': ("challenge yourself with complex reading materials", "reading-materials")
        }
    
        "You must focus more on past tense usage including all the modifier like past continous, past future, and past present. You can learn on our website at smartengtest/past-tense."
        "You must focus more on past tense usage including all the modifier like past continous, past future, and past present. You can learn on our website at smartengtest/past-tenses."
        paired_actions = {
            ('past', 'tenses types'): "focus more on past tense usage including all the modifier like past continous, past future, and past present",
            ('tenses types', 'past'): "focus more on past tense usage including all the modifier like past continous, past future, and past present",
        }    

        if (antecedent, consequent) in paired_actions:
            action = paired_actions[(antecedent, consequent)]
            # Assuming the consequent is a key in the actions dictionary for the URL slug
            # If not, add a default slug here
            slug = actions.get(consequent, ("past-tenses", ""))[1]
        elif antecedent in actions:
            action, slug = actions[antecedent]
        else:
            # Default action and slug if no match is found
            action, slug = "perform the relevant activity", "general"

        return action, slug