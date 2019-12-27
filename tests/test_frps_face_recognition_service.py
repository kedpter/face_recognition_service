#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `face_recognition_service` package."""

from unittest import TestCase
# from face_recognition_service.api import face_module
# from face_recognition_service.
import tempfile
import io
import os
import numpy as np
from flask import json

from face_recognition_service.api import app, api
from face_recognition_service.resources.conversion import Conversion
from face_recognition_service.resources.encodings import FaceEncodingList, FaceEncoding
from face_recognition_service.face_engine import FaceEngine
from face_recognition_service.resources.comparison import CompareDistances
from face_recognition_service.resources.configuration import Configuration


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestConversion(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_api_post_conversion_encoding(self):
        img_file = '{0}/test_files/biden.jpg'.format(BASE_DIR)
        with open(img_file, 'rb') as img:
            bytes = img.read()

        data = {
            # 'face_image': (io.BytesIO(b'content'), '1.jpg')
            'face_image': (io.BytesIO(bytes), '1.jpg')
        }

        with app.test_request_context():
            response = self.client.post(api.url_for(Conversion), buffered=True,
                                        content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)


class TestEncodings(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_api_delete_encodings(self):
        engine = FaceEngine()
        engine.add_face('1', 'face encoding')
        with app.test_request_context():
            response = self.client.delete(api.url_for(FaceEncodingList))
            self.assertEqual(response.status_code, 200)

        self.assertTrue(len(engine.faces) == 0)

    def test_api_post_encodings(self):
        engine = FaceEngine()

        np_file = '{0}/test_files/face.dat'.format(BASE_DIR)
        with open(np_file, 'rb') as f:
            bytes = f.read()
        data = {
            'id': 1,
            'encoding_file': (io.BytesIO(bytes), '1.dat')
        }
        with app.test_request_context():
            response = self.client.post(api.url_for(FaceEncodingList),
                                        buffered=True, content_type='multipart/form-data', data=data)
            self.assertTrue(response.status_code, 200)
            face_exists = any([x.id == 1 for x in engine.faces])
            self.assertTrue(face_exists)


class TestEncoding(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_api_delete_encodings_id(self):
        engine = FaceEngine()
        engine.delete_all_encodings()
        engine.add_face('1', 'encoding')

        with app.test_request_context():
            response = self.client.delete(api.url_for(FaceEncoding, encoding_id='1'))
            self.assertTrue(response.status_code, 200)
            self.assertEqual(len([x.id == 1 for x in engine.faces]), 0)


class TestComparison(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_post_comparison_distances(self):
        engine = FaceEngine()
        img_file = '{0}/test_files/biden.jpg'.format(BASE_DIR)

        image = engine.load_image_file(img_file)
        known_face_encoding = engine.face_encodings(image)[0]
        engine.add_face('1', known_face_encoding)

        np_file = '{0}/test_files/face.dat'.format(BASE_DIR)
        with open(np_file, 'rb') as f:
            bytes = f.read()
        data = {
            'tolerance': 0.6,
            'unknown_dat': (io.BytesIO(bytes), '1.dat')
        }
        with app.test_request_context():
            response = self.client.post(api.url_for(CompareDistances),
                                        buffered=True, content_type='multipart/form-data', data=data)
            self.assertTrue(response.status_code, 200)


def convert(client, img_file, id):
    # img_file = '{0}/test_files/biden.jpg'.format(BASE_DIR)
    with open(img_file, 'rb') as img:
        bytes = img.read()

    data = {
        # 'face_image': (io.BytesIO(b'content'), '1.jpg')
        'face_image': (io.BytesIO(bytes), '1.jpg')
    }

    with app.test_request_context():
        response = client.post(api.url_for(Conversion), buffered=True,
                               content_type='multipart/form-data', data=data)
        encoding_file = '{0}/{1}.dat'.format(BASE_DIR, str(id))
        with open(encoding_file, 'wb') as f:
            f.write(response.data)

        return encoding_file


def add_encoding(client, id, encoding_file):
    # np_file = '{0}/test_files/face.dat'.format(BASE_DIR)
    np_file = encoding_file
    with open(np_file, 'rb') as f:
        bytes = f.read()
    data = {
        'id': id,
        'encoding_file': (io.BytesIO(bytes), '1.dat')
    }
    with app.test_request_context():
        response = client.post(api.url_for(FaceEncodingList),
                               buffered=True, content_type='multipart/form-data', data=data)


class IntegrationTest(TestCase):
    def setUp(self):
        self.client = app.test_client()

        biden2_img = '{}/test_files/biden2.jpg'.format(BASE_DIR)
        biden2_id = 300

        obama_img = '{}/test_files/obama.jpg'.format(BASE_DIR)
        biden_img = '{}/test_files/biden.jpg'.format(BASE_DIR)
        obama_id = 100
        biden_id = 200
        self.obama_id = obama_id
        self.biden_id = biden_id

        imgs = [obama_img, biden_img]
        ids = [obama_id, biden_id]

        # convert imgs to encodings
        encoding_files = [convert(self.client, x[0], x[1]) for x in zip(imgs, ids)]

        # add encodings to engine
        [add_encoding(self.client, x[0], x[1]) for x in zip(ids, encoding_files)]

        # compare biden2 with known faces
        self.biden2_encoding_file = convert(self.client, biden2_img, biden2_id)

    def test_compare_biden2_with_known_faces(self):
        np_file = self.biden2_encoding_file
        with open(np_file, 'rb') as f:
            bytes = f.read()
        data = {
            'tolerance': 0.6,
            'unknown_dat': (io.BytesIO(bytes), '1.dat')
        }
        with app.test_request_context():
            response = self.client.post(api.url_for(CompareDistances),
                                        buffered=True, content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)
            dist_json = json.loads(response.get_data(as_text=True))
            biden_id_exists = str(self.biden_id) in dist_json
            self.assertTrue(biden_id_exists)


class ConfigurationTest(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_api_configuration(self):
        engine = FaceEngine()
        with app.test_request_context():
            response = self.client.put(api.url_for(Configuration),
                                       query_string={'enable_cnn': True})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(engine.enable_cnn, True)
