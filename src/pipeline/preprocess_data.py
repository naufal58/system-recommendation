from src.controllers.data_preprocess import DataPreprocess

def start(filename):
    data_preprocess = DataPreprocess(filename)
    data_preprocess.convert_to_json()
    data_preprocess.replace_missing_symbols()
    data_preprocess.get_underlines()
    data_preprocess.check_answer_result()
    return True
