from flask import Flask
from flask_cors import CORS
from Routes import register_blueprints


app = Flask(__name__)
register_blueprints(app)

CORS(app)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
