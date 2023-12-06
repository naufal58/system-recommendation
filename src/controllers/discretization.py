
class Discretization():
    def __init__(self, data):
        self.data = data

    def normalize(self, value, min_value, max_value) -> float:
        return float((value - min_value) / (max_value - min_value))

    def normalize_numeric(self):
        attributes = ['conjunctions', 'flesch_reading_ease']
        for i in attributes:
            value = [temp[i] for temp in self.data]
            for item in self.data:
                item[i] = round(self.normalize(item[i], min(value), max(value)), 3)

        return True
    
    def remove_correct_answers(self):
        wrong_answers = []
        for item in self.data:
            if item['result'] == 0:
                del item['result']
                wrong_answers.append(item)
        return wrong_answers