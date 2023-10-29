from models.feature_extraction import *

class DemoPipeline:
    def __init__(self, text):
        self.text = text
    
    def get_homophones(self):
        homophones = count_homophones(self.text)

        return homophones

if __name__ == '__main__':
    demo_pipeline = DemoPipeline("It's always a good idea to seek shelter from the evil gaze of the sun.")
    print(demo_pipeline.get_homophones())