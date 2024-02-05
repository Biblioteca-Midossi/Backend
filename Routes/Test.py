from flask import jsonify
from flask import Blueprint
from Utils.Database.DbHelper import Database

test = Blueprint('Test', __name__)


@test.route('/api/test')
def test_route():
    return jsonify({'message': 'Test route works! Now try the others! 💀'}), 200


@test.route('/api/get-test')
def db_get_test():
    with Database() as db:
        cursor = db.get_cursor()
        cursor.execute("select * from biblioteca.test")
        test_result = [{
            'test': result[0],
        } for result in cursor.fetchall()]
        return jsonify(test_result)
