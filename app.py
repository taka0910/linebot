from flask import Flask
app = Flask(__name__)

@app.route('/', methods=["POST"])
def hello_world():
    return str(request.form)
