from flask import jsonify, Blueprint
from Utils.Database.DbHelper import Database

from time import time


class Test(Blueprint):
    def __init__(self, name):
        super().__init__(name, __name__)

        @self.route('/api/test')
        def test_route():
            return jsonify({'message': 'Test route works! Now try the others! 💀'}), 200

        @self.route('/api/get-test')
        def db_get_test():
            print(round(time() * 1000))
            with Database() as db:
                cursor = db.get_cursor()
                cursor.execute("select * from biblioteca.test")
                print(round(time()*1000))
                test_result = [{
                    'test': result[0],
                } for result in cursor.fetchall()]
            return jsonify(test_result)
