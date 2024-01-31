from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/test', methods=['GET'])
def hello():
    return jsonify({'message': 'Test route works! Now try the others! 💀'}), 200


if __name__ == '__main__':
    app.run()
