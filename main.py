import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from Routes.Test import test

# Create `app` beforehand, so you can pass it to Routes.
app = Flask(__name__)
app.register_blueprint(test)
CORS(app)


if __name__ == '__main__':
    app.run(debug = True)
