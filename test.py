from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def puzzle():
    response = {"running": "True"}
    return jsonify(response), 200

app.run(host='0.0.0.0', port=80)
