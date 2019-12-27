# -*- coding: utf-8 -*-
'''
This module functions as an adapter. It will direct user request to specific api controller
'''

from flask import Flask
from flask_restful import Resource, Api
import os
# from face_recognition_service.resources.encoding import FaceEncodingListInitApi, FaceEncodingListApi, FaceEncodingApi
# from face_recognition_service.resources.recognition import FaceRecognitionApi
from face_recognition_service.resources.encodings import FaceEncodingList, FaceEncoding
from face_recognition_service.resources.conversion import Conversion
from face_recognition_service.resources.comparison import CompareDistances
from face_recognition_service.resources.configuration import Configuration
from face_recognition_service.resources.example_page import ExamplePage

app = Flask(__name__, static_folder="static")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
app.config['convert_faces_dir'] = '{}/static/convert_faces'.format(BASE_DIR)
api = Api(app)


__version__ = 'v1'

api_version = '/{0}/{1}'.format('api', __version__)
face_module = '{0}/{1}'.format(api_version, 'face')


api.add_resource(FaceEncodingList, '{0}/encodings'.format(face_module))

api.add_resource(FaceEncoding, '{0}/encodings/<encoding_id>'.format(face_module))

api.add_resource(Conversion, '{0}/conversions/encoding'.format(face_module))

api.add_resource(CompareDistances, '{0}/comparison/distances'.format(face_module))

api.add_resource(Configuration, '{0}/configuration'.format(face_module))

api.add_resource(ExamplePage, '/')
# api.add_resource(
#     HelloWorld, '/{0}/{1}/test'.format(ApiUrlConstants.Api, ApiUrlConstants.Version))
# api.add_resource(
#     FaceEncodingListInitApi, '/{0}/{1}/face_encodings/init'.format(ApiUrlConstants.Api, ApiUrlConstants.Version))
# api.add_resource(
#     FaceEncodingListApi, '/{0}/{1}/face_encodings'.format(ApiUrlConstants.Api, ApiUrlConstants.Version))
# api.add_resource(
#     FaceRecognitionApi, '/{0}/{1}/face'.format(ApiUrlConstants.Api, ApiUrlConstants.Version))
