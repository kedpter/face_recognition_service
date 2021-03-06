from flask_restful import Resource, reqparse
from flask import json, Response
import werkzeug
import tempfile

from face_recognition_service.face_engine import FaceEngine
from face_recognition_service.models.face import DbException
import numpy as np
import os
import uuid
from flask import send_file, current_app as app


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
        # parse.add_argument('id', type=int, required=True, location='form')
        parse.add_argument('id', required=True, location='form')
        parse.add_argument(
            'encoding_file', required=True, type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        engine = FaceEngine()

        filename = os.path.join(app.config['convert_faces_dir'], '{}.ecdtmp'.format(uuid.uuid1()))


        try:
            with open(filename, 'wb') as tmp:
                tmp.write(args['encoding_file'].read())

            face_encoding = np.load(filename, allow_pickle=True)
        finally:
            os.unlink(filename)

        try:
            engine.add_face(args['id'], face_encoding)
        except DbException as e:
            msg = {'message': str(e)}
            return Response(
                response=json.dumps(
                    msg
                ),
                status=500,
                mimetype="application/json"
            )

        # with tempfile.NamedTemporaryFile(delete=False) as tmp:
        #     tmp.write(args['encoding_file'].read())
        #     tmp.flush()
        #     tmp.seek(0)
        #     face_encoding = np.load(tmp.name, allow_pickle=True)

        #     tmp.close()
        #     os.unlink(tmp.name)

        #     try:
        #         engine.add_face(args['id'], face_encoding)
        #     except DbException as e:
        #         msg = {'message': str(e)}
        #         return Response(
        #             response=json.dumps(
        #                 msg
        #             ),
        #             status=500,
        #             mimetype="application/json"
        #         )


class FaceEncoding(Resource):
    def delete(self, encoding_id):
        '''
        delete encoding by id
        '''
        engine = FaceEngine()
        engine.delete_by_id(encoding_id)
        pass
