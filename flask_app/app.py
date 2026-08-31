from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def receive_data():
    return jsonify({"msg": "Hello, World!"}), 200