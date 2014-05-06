

from uuid import uuid4 as uuid
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/users', methods=['POST'])
def users():
    data = request.get_json()
    data['id'] = uuid()  # predstirame ukladani do databaze
    return jsonify(data), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
