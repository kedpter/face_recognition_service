from flask_restful import Resource, reqparse
import werkzeug
import tempfile
import numpy as np
import uuid

# from face_recognition_service.api import app
from face_recognition_service.face_engine import FaceEngine
from flask import send_file, current_app as app
import os


class Conversion(Resource):
    def post(self):
        '''
        post an image file
        return a file of numpy face encoding array
        '''
        parse = reqparse.RequestParser()
        parse.add_argument('face_image', required=True,
                           type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        engine = FaceEngine()

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            # with open('upload.jpg', 'wb') as tmp:
            file = args['face_image']
            tmp.write(file.read())
            tmp.flush()

            image = engine.load_image_file(tmp.name)

            # fix tempfile bug
            tmp.close()
            os.unlink(tmp.name)

            encodings = engine.face_encodings(image)
            if len(encodings) == 0:
                return {'success': 'false', 'reason': 'no face in image'}

            # choose the first face
            encoding = encodings[0]

            np_file = '{0}/{1}.npy'.format(app.config['convert_faces_dir'], uuid.uuid1())
            np.save(np_file, encoding)
            # encoding.dump(np_file)
            file_handle = open(np_file, 'rb')

            def stream_and_remove_file():
                yield from file_handle  # noqa
                file_handle.close()
                os.remove(np_file)

            return app.response_class(
                stream_and_remove_file(),
                mimetype='octet-stream',
                headers={'Content-Disposition': 'attachment', 'filename': 'face.dat'}
            )
