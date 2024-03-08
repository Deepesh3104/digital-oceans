from flask import Flask, render_template, request, jsonify
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from chat import get_response
import torch
import json
import random

app = Flask(__name__)



@app.get('/')
def index_get():
    return render_template('base.html')

@app.post("/predicti")
def predicti():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True, port = 5000)