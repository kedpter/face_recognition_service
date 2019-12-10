
from __future__ import print_function
import sys
import face_recognition
from face_recognition_service.models.database import MemDatabase
from face_recognition_service.models.face import Face


class FaceEngine:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        # self.state = 'Init'

        self.load_image_file_mode = 'RGB'
        self.tolerance = 0.6
        self.enable_cnn = False
        self.__db = MemDatabase()
        self.debug = True

    @property
    def faces(self):
        return self.__db.face_dao.find_all()

    # def __str__(self):
    #     return self.state

    def load_image_file(self, file):
        return face_recognition.load_image_file(file, self.load_image_file_mode)

    # def compare_faces(self, known_face_encodings, face_encoding_to_check):
    #     return face_recognition.compare_faces(known_face_encodings, face_encoding_to_check, self.tolerance)

    def face_encodings(self, face_image, known_face_locations=None, num_jitters=1):
        '''
        :return: A list of 128-dimensional face encodings (one for each face in the image)
        '''
        if self.enable_cnn and known_face_locations is None:
            known_face_locations = face_recognition.face_locations(face_image, model="cnn")
        return face_recognition.face_encodings(face_image, known_face_locations, num_jitters)

    def face_distance(self, face_to_compare):
        '''
        Given a list of face encodings from database, compare them to a known face encoding and get a euclidean distance
        for each comparison face. The distance tells you how similar the faces are.

        :param face_to_compare: A face encoding to compare against
        :return: a json array with id and distance
        '''
        face_encodings = [x.encoding for x in self.faces]
        distances = face_recognition.face_distance(face_encodings, face_to_compare)
        result = {}
        for x in zip(self.faces, distances):
            result[x[0].id] = x[1]
        return result

    def compare_faces(self, face_distances):
        if self.debug:
            print('compare face', file=sys.stdout)
        return list(face_distances <= self.tolerance)

    def delete_all_encodings(self):
        self.__db.face_dao.delete_all()
        if self.debug:
            print('delete all faces', file=sys.stdout)

    def delete_by_id(self, id):
        self.debug
        self.__db.face_dao.delete_by_id(id)
        if self.debug:
            print('delete face: {}'.format(id), file=sys.stdout)

    def add_face(self, id, encoding):
        f = Face(id, encoding)
        self.__db.face_dao.append(f)
        if self.debug:
            print('add face: {}'.format(id), file=sys.stdout)
