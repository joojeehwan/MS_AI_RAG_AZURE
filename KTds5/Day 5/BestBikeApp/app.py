from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "집에 가고 싶다!\n"