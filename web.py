

import os
import json
from uuid import uuid4 as uuid
from flask import Flask, request, jsonify
from jsonschema import Draft4Validator as Validator, RefResolver


app = Flask(__name__)


def validate(schema_filename, data):
    with open(schema_filename) as f:
        schema = json.load(f)  # cteme JSON Schema primo ze souboru
    Validator.check_schema(schema)  # zkontroluje schema nebo vyhodi vyjimku

    base_uri = 'file://' + os.path.dirname(schema_filename) + '/'
    resolver = RefResolver(base_uri, schema)
    validator = Validator(schema, resolver=resolver)
    return validator.iter_errors(data)  # vraci chyby jednu po druhe


@app.route('/users', methods=['POST'])
def users():
    data = request.get_json()

    schema_filename = os.path.join(app.root_path, 'user.json')
    errors = [error.message for error in validate(schema_filename, data)]
    if errors:
        return jsonify(errors=errors), 400

    data['id'] = uuid()  # predstirame ukladani do databaze
    return jsonify(data), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
