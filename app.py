from flask import Flask, request
from src.utils.db import db
# Import controllers
from src.controllers.recommendation import Recommendation
from src.pipeline.extract_features import extract_features
from src.utils.helper_functions import demo_extract

app = Flask(__name__)
app.config.from_object('src.utils.setting.Config')

# initialization
# db.init_app(app)

@app.route("/")
def hello_world():
    return {'msg': "Hello World!"}

@app.route("/demo", methods=['GET'])
def demo_extract_features_pipeline():
    pipeline = extract_features("These television are all to expensive for we to buy at this time, but perhaps we will return later", [0, 4, 7, 11])
    if pipeline:
        return pipeline
    else:
        return {'msg': 'there is an error!'}

@app.route("/demo/database", methods=['GET'])
def demo_pipeline_database():
    n_question = int(request.form['max'])
    pipeline = demo_extract(n_question, shuffle=True)
    return {'msg': pipeline}

# adding routes
app.add_url_rule('/recommendation/<int:id>', view_func=Recommendation.recommendation, methods=['GET',])

#run
if __name__ == '__main__':
    # Change the port to 5006
    app.run(debug=True, port=5006)
