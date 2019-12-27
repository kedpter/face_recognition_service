class DbException(Exception):
    pass


class Face:
    def __init__(self, id, encoding):
        self.id = id
        self.encoding = encoding

    def __str__(self):
        return '[id]: {0}\n[encoding]: {1}'.format(self.id, self.encoding)


class FaceDao:
    def __init__(self):
        self.__faces = []

    def __validate(self, obj):
        if not isinstance(obj, Face):
            raise DbException("Not a Face object")
        if any(x.id == obj.id for x in self.__faces):
            raise DbException("id ({}) already exists".format(obj.id))

    def append(self, obj):
        self.__validate(obj)
        self.__faces.append(obj)
        pass

    def extend(self, obj_list):
        for obj in obj_list:
            self.__validate(obj)
        self.__faces.extend(obj_list)

    def delete_by_id(self, id):
        self.__faces = [f for f in self.__faces if f.id != id]

    def delete_all(self):
        self.__faces = []

    def find_all(self):
        return self.__faces
