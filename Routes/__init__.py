from flask import jsonify
from .Test import Test


def register_blueprints(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'error': 'Page not found'}), 400

    app.register_blueprint(Test('Test'))
