from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def puzzle():
    response = {"running": "True"}
    return jsonify(response), 200

app.run(host='0.0.0.0', port=80)
