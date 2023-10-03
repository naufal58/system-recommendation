from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    # Change the port to 5006
    app.run(host='0.0.0.0', port=5006)
