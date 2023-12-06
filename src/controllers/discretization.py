
class Discretization():
    def __init__(self, data):
        self.data = data

    def normalize(self, value, min_value, max_value) -> float:
        return float((value - min_value) / (max_value - min_value))

    def normalize_numeric(self):
        attributes = ['irregular_verbs', 'regular_verbs', 'homophones', 'conjunctions', 'flesch_reading_ease']
        for i in attributes:
            value = [temp[i] for temp in self.data]
            for item in self.data:
                item[i] = round(self.normalize(item[i], min(value), max(value)), 3)

        return True
    
    def discrete_categorical(self):
        for item in self.data:
            if item['tense_type'] == 'future':
                item['tense_type'] = 0.0
            elif item['tense_type'] == 'past':
                item['tense_type'] = 1.0
            else:
                item['tense_type'] = 2.0

        return True