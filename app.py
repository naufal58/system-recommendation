from flask import Flask
from pipeline.demo import DemoPipeline
from pipeline.utility import demo_extract

app = Flask(__name__)

@app.route("/")
def hello_world():
    return {'msg': "Hello World!"}

@app.route("/demo", methods=['GET'])
def demo_pipeline():
    demo_pipeline = DemoPipeline("It's always a good idea to seek shelter from the evil gaze of the sun.")
    return demo_pipeline.pipeline()

@app.route("/demo/database", methods=['GET'])
def demo_pipeline_database():
    demo_pipeline = demo_extract(5)
    return {'msg': demo_pipeline}

if __name__ == '__main__':
    # Change the port to 5006
    app.run(debug=True, port=5006)
