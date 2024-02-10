from flask import jsonify, Blueprint


class Insert(Blueprint):
    def __init__(self, name):
        super().__init__(name, __name__)
