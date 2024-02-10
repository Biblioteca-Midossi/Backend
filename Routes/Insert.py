from flask import jsonify, Blueprint, request, make_response


class Insert(Blueprint):
    def __init__(self, name):
        super().__init__(name, __name__)

        @self.route("/api/insert", methods = ['POST', 'OPTIONS'])
        def insert():
            if request.method == "OPTIONS":
                response = make_response()
                response.headers.add('Access-Control-Allow-Methods', 'POST')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response

            data = request.get_json()

            print(data)

            return jsonify({"status": "successful"}), 200
