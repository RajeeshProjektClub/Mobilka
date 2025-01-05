from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return{"data": "TwojaStara"}
    
api.add_resource(HelloWorld, "/helloworld/<int>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2234, debug=True)