from face_recognition_service.models.face import FaceDao
from face_recognition_service.util.singleton import Singleton


class MemDatabase(metaclass=Singleton):  # noqa
    def __init__(self):
        # self.known_userencs_dao = UserEncDao()
        self.face_dao = FaceDao()
        pass

    def __str__(self):
        return '\n'.join([str(u) for u in self.face_dao.findall()])
