from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
#db.create_all() # run this line only once, if we run more the once the database wi be overwritten

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False) # nullable = False, means that we can't have a video without a name
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self) -> str:
		return f"Video(name={self.name}, views={self.views}, likes={self.likes}"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="name of the video", required=True)
video_put_args.add_argument("views", type=int, help="views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="name of the video")
video_update_args.add_argument("views", type=int, help="views of the video")
video_update_args.add_argument("likes", type=int, help="likes of the video")
# Define the fields of a model that I want to return if I return a especific object
resource_field = {
	'id' : fields.String,
	'name' : fields.String,
	'views' : fields.Integer,
	'likes' : fields.Integer
}

class Video(Resource):
	@marshal_with(resource_field)
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Couldn't find this id...")
		return result

	@marshal_with(resource_field)
	def put(self,  video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.get(id=video_id).first()
		if result:
			abort(409, message='Video id aready taken...')
		new_video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes']) # creating a new video extracting informations from the url
		db.session.add()
		db.session.commit()
		return new_video, 201 # returning the video and the status code

	def patch(self, video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()

	def delete(self, video_id):
		VideoModel.query.filter_by(id=video_id).delete()
		db.session.commit()
		return '', 204
	
api.add_resource(Video, '/video/<int:video_id>') # (resource, key)

if __name__ == '__main__':
	app.run(debug=True)