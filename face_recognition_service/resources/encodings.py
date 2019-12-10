from flask_restful import Resource, reqparse
import werkzeug
import tempfile

from face_recognition_service.face_engine import FaceEngine
import numpy as np


class FaceEncodingList(Resource):
    def delete(self):
        '''
        delete all encodings
        '''
        engine = FaceEngine()
        engine.delete_all_encodings()
        pass

    def post(self):
        '''
        add an encoding
        '''
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, required=True, location='form')
        parse.add_argument(
            'encoding_file', required=True, type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        engine = FaceEngine()

        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(args['encoding_file'].read())
            tmp.flush()
            tmp.seek(0)
            face_encoding = np.load(tmp.name, allow_pickle=True)
            engine.add_face(args['id'], face_encoding)


class FaceEncoding(Resource):
    def delete(self, encoding_id):
        '''
        delete encoding by id
        '''
        engine = FaceEngine()
        engine.delete_by_id(encoding_id)
        pass
