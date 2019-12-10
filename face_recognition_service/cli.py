from face_recognition_service.api import app
from face_recognition_service.face_engine import FaceEngine
import os


def main():
    app.debug = True
    FaceEngine().debug = True
    # app.config['DATABASE_NAME'] = 'library.db'
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
