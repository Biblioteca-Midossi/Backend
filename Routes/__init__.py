from flask import jsonify
from .Test import Test
from .Insert import Insert


def register_blueprints(app):
    @app.errorhandler(404)
    def page_not_found():
        return jsonify({'error': 'Page not found'}), 400

    app.register_blueprint(Test('Test'))
    app.register_blueprint(Insert('Insert'))
