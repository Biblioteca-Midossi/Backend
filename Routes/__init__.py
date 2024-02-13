from flask import jsonify, Flask
from .Test import Test
from .Insert import Insert


def register_blueprints(app: Flask):

    # Try putting these in a class where you pass `app`
    # to initialize it and then register as a Blueprint.
    # Also substitute Blueprints with Flask RESTful
    # (Check performance comparison before doing)
    # Also take a look at Quart and Falcon libraries.
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'error': f'{error}'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': f'{error}'}), 500

    app.register_blueprint(Test('Test'))
    app.register_blueprint(Insert('Insert'))
