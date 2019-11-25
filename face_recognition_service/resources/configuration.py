from flask_restful import Resource, reqparse, inputs

from face_recognition_service.face_engine import FaceEngine


class Configuration(Resource):
    def put(self):
        parse = reqparse.RequestParser()
        parse.add_argument('enable_cnn', type=inputs.boolean, required=True, location='args')
        args = parse.parse_args()

        engine = FaceEngine()
        engine.enable_cnn = args['enable_cnn']
        # if args['enable_cnn'] is not None:
