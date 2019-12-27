from flask_restful import Resource, reqparse
import werkzeug
import tempfile
from flask import render_template, make_response


class ExamplePage(Resource):
    def __init__(self):
        pass

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
