from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
import pandas as pd
from itertools import combinations, chain
from pyECLAT import ECLAT
from collections import OrderedDict
import itertools
from sklearn.preprocessing import MultiLabelBinarizer
from src.utils.helper_functions import get_training_data

class Recommendation():
    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        data_temp = get_training_data(self.filename)
        data = data_temp['data']
        df = pd.DataFrame(data)
        
        for col in df.columns:
            if df[col].dtype == bool:
                df[col] = df[col].astype(int)
                
        df = df[df['result'] == 0].drop(['nama', 'result', 'soal'], axis=1)
        df.reset_index(drop=True, inplace=True)

        new_df = df.apply(lambda row: pd.Series(row[row == 1].index.values), axis=1)

        comp_series = new_df.stack().reset_index(drop=True)
        
        comp_count = comp_series.value_counts()
        
        comp_percentage = (comp_count / len(df)) * 100

        return new_df, comp_percentage

    def find_frequent_itemsets(self, min_support=0.08, min_confidence = 0.9):
        transactions ,_ = self.get_data()
        print(transactions)

        # Assume transactions is a list of lists
        dataset = pd.DataFrame(transactions)
        eclat_instance = ECLAT(data=dataset, verbose=True)

        items_total = eclat_instance.df_bin.astype(int).sum(axis=0)

        items_per_transaction = eclat_instance.df_bin.astype(int).sum(axis=1)

        # Determine the maximum items per transaction
        max_combination = max(items_per_transaction)
        
        # Fit the model with the specified parameters
        rule_indices, rule_supports = eclat_instance.fit(min_support=min_support,
                                                         min_combination=1,
                                                         max_combination=max_combination,
                                                         separator=' & ',
                                                         verbose=True)
        
        rules_with_confidence = []
        # Generate association rules
        for itemset, support in rule_supports.items():
            items = itemset.split(' & ')
            for i in range(1, len(items)):
                for antecedent in itertools.combinations(items, i):
                    antecedent_str = ' & '.join(antecedent)
                    consequent = set(items) - set(antecedent)
                    consequent_str = ' & '.join(consequent)
                    antecedent_support = rule_supports.get(antecedent_str, 0)
                    if antecedent_support > 0:
                        confidence = support / antecedent_support
                        if confidence >= min_confidence:
                            rules_with_confidence.append({
                                'Antecedent': antecedent_str,
                                'Consequent': consequent_str,
                                'Support': support,
                                'Confidence': confidence
                            })
        
        rules_df = pd.DataFrame(rules_with_confidence)
        rules_df = rules_df.sort_values(by='Confidence', ascending=False)
        return rules_df
        
    def learning_material_mapping(self):
        # This dictionary maps competencies to learning materials
        learning_materials = {
            'irregular_past_form': [
                'Past Tense',
                'Irregular Verbs'
            ],
            'gerund_requirement': [
                'Gerunds Usage',
                'Gerunds vs Participles'
            ],
            'infinitive_requirement': [
                'Infinitives Usage',
                'Bare vs To-Infinitive'
            ],
            'singular_expression': [
                'Singular Nouns and Verbs'
            ],
            'plural_expression': [
                'Plural Nouns and Verbs'
            ],
            'gerund_phrase_requirement': [
                'Gerund Phrases Construction and Functions'
            ],
            'importance_subjunctive_verb': [
                'Subjunctive Mood and Uses'
            ],
            'past_participle': [
                'Forming Past Participles',
                'Past Participles Usage'
            ],
            'factual_conditional': [
                'Zero and First Conditional'
            ],
            'relative_pronouns': [
                'Pronouns Usage',
                'Sentence Combining'
            ],
        }

        lowercase_materials = {key: [phrase.lower() for phrase in value] for key, value in learning_materials.items()}
        return lowercase_materials  

    def generate_numbered_tiered_recommendations(self):
        rules_df = self.find_frequent_itemsets(min_support=0.08, min_confidence=0.9)
        _, comp_percentage = self.get_data()
        print(comp_percentage)
        learning_materials_mapping = self.learning_material_mapping()

        global_materials_covered = set()

        recommendations = []
        recommendation_counter = 1

        # Iterate through each rule in the DataFrame
        for _, rule in rules_df.iterrows():
            antecedent = rule['Antecedent']
            consequent = rule['Consequent']
            antecedent_percentage = comp_percentage.get(antecedent, 0)
            consequent_percentage = comp_percentage.get(consequent, 0)

            # Determine the priority level for antecedent and consequent
            antecedent_priority = 'crucial' if antecedent_percentage >= 80 else 'important' if antecedent_percentage >= 40 else 'recommended'
            consequent_priority = 'crucial' if consequent_percentage >= 80 else 'important' if consequent_percentage >= 40 else 'recommended'

            # Initialize a dictionary to hold current rule's learning materials and priorities
            current_rule_materials = {}
            
            # Process antecedent and consequent competencies
            for comp in antecedent.split(" & ") + consequent.split(" & "):
                for mat in learning_materials_mapping.get(comp, [comp]):
                    if mat not in global_materials_covered:
                        priority = antecedent_priority if comp in antecedent else consequent_priority
                        current_rule_materials[mat] = priority

            # Skip this rule if all materials have been covered
            if not current_rule_materials:
                continue

            # Group materials by priority and sort
            priority_groups = {'crucial': [], 'important': [], 'recommended': []}
            for mat, priority in current_rule_materials.items():
                priority_groups[priority].append(mat)
                global_materials_covered.add(mat)  # Mark materials as covered

            # Constructing the recommendation string with grouped priorities
            recommendation_str_parts = []
            for priority in ['crucial', 'important', 'recommended']:  # Ensure priority order
                mats = priority_groups[priority]
                if mats:
                    mats.sort()  # Sort materials alphabetically within the same priority level
                    mats_str = ", ".join(mats)
                    part = f"{priority} for you to learn {mats_str}"
                    recommendation_str_parts.append(part)

            # Join parts with correct formatting and add to recommendations list
            if recommendation_str_parts:
                recommendation_str = "It is " + ", and ".join(recommendation_str_parts) + "."
                recommendations.append(f"{recommendation_counter}. {recommendation_str}")
                recommendation_counter += 1

        return recommendations[:3]
    
    def competencies(self):
        # Get the mapping of competencies to learning materials
        mapping = self.learning_material_mapping()
        rules_df = self.find_frequent_itemsets()
        print(rules_df)

        def map_competency_to_materials(competency, mapping):
            # Split the competency string into individual competencies if there are multiple
            competencies = competency.split(' & ')
            # Map each competency to its learning materials, joining them with ', '
            materials = [', '.join(mapping.get(comp, ['No material found'])) for comp in competencies]
            # Join all learning materials for the competencies with '; ' to differentiate between different competencies
            return '; '.join(materials)

        # Replace competencies in 'Antecedent' and 'Consequent' with learning materials
        rules_df['Antecedent'] = rules_df['Antecedent'].apply(map_competency_to_materials, args=(mapping,))
        rules_df['Consequent'] = rules_df['Consequent'].apply(map_competency_to_materials, args=(mapping,))

        # Now rules_df contains rules with competencies replaced by their corresponding learning materials
        return rules_df

        # # Get the top 3 competencies based on count
        # top_competencies = competency_counts.head(3).index.tolist()

        # # Select the learning materials associated with the top 3 competencies
        # top_learning_materials = {comp: learning_materials[comp] for comp in top_competencies if comp in learning_materials}

        # # Sort the learning materials for each competency based on their associated competency counts
        # for competency in top_learning_materials:
        #     top_learning_materials[competency].sort(key=lambda x: competency_counts.get(competency), reverse=True)

        # # Create an ordered dictionary of the top 3 competencies and their sorted learning materials
        # sorted_learning_materials = OrderedDict((comp, top_learning_materials[comp]) for comp in top_competencies if comp in top_learning_materials)

        # return sorted_learning_materials
    
    
    # def get_actions(self):
    #     return {
    #         'tenses types': ("learn more about modifier tenses", "past-tense"),
    #         'past': ("focus more on past tense usage including all the modifiers like past continuous, past future, and past present", "past-tense"),
    #         'present': ("concentrate on present tense structures", "present-tense"),
    #         'future': ("prepare for future tense scenarios", "future-tense"),
    #         'l_vocabulary_difficulty_score': ("enhance basic vocabulary skills", "vocabulary"),
    #         'm_vocabulary_difficulty_score': ("build on intermediate vocabulary", "vocabulary"),
    #         'h_vocabulary_difficulty_score': ("master advanced vocabulary", "vocabulary"),
    #         'l_conjunctions': ("practice basic conjunctions", "conjunctions"),
    #         'm_conjunctions': ("improve use of intermediate conjunctions", "conjunctions"),
    #         'h_conjunctions': ("refine usage of complex conjunctions", "conjunctions"),
    #         'l_flesch_reading_ease': ("read simpler texts to improve comprehension", "reading-materials"),
    #         'm_flesch_reading_ease': ("engage with moderately complex texts", "reading-materials"),
    #         'h_flesch_reading_ease': ("challenge yourself with complex reading materials", "reading-materials")
    #     }

    # def generate_recommendation(self, filtered_rules):
    #     actions = self.get_actions()
    #     recommendations = []

    #     for index, rule in filtered_rules.iterrows():
    #         antecedents = ', '.join(list(rule['antecedents']))
    #         consequents = ', '.join(list(rule['consequents']))

    #         antecedent_action, antecedent_slug = actions.get(antecedents, ("", ""))
    #         consequent_action, consequent_slug = actions.get(consequents, ("", ""))

    #         recommendation = f"You should {antecedent_action}. Additionally, to enhance your skills you should {consequent_action}. Learn more at smartengtest/{antecedent_slug} and smartengtest/{consequent_slug}."
    #         recommendations.append(recommendation)
        
    #     return recommendations

    