from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

'''
names = {"tim": {"age": 19, "gender": "male"},
         "jake":{"age": 70, "gender": "male"}}
class HelloWorld(Resource):
    def get(self, name):
        return{"data": name}
api.add_resource(HelloWorld, "/helloworld/<string:name>")
'''

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video")
video_put_args.add_argument("views", type=str, help="Name of the video")
video_put_args.add_argument("likes", type=str, help="Name of the video")

videos = {}

def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video is not valid...")

def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID..,")

class Video(Resource):
    def get (self, video_id):
        return videos[video_id]
    
    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
    
    def delete(self, video_id):


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=2234, debug=True)
    app.run(debug=True)