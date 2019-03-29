import json
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
# Uncomment this line if you are making a Cross domain request
CORS(app)

@app.route('/classifier-predict/', methods=['POST'])
def image_classifier():
    payload = None
    if request.data:
        payload = json.loads(request.data)
    if request.form:
        payload = request.form['instances[0][image_bytes][b64]']
        payload = payload.split("base64,")[1]
        payload = {
            "instances": [{'image_bytes': {'b64': payload}}]
        }

    r = requests.post(
        'http://localhost:8501/v1/models/tfserving_dogs_cats_models:predict',
        json=payload)
    pred = json.loads(r.content.decode('utf-8'))

    return jsonify(pred)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
