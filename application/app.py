from flask import Flask, request
from endpoints import api
from utils import request_parser


parser_vr = request_parser.parser_vr
vr_choices = request_parser.fields_choices
parser_vv = request_parser.parser_vv
parser_vep = request_parser.parser_vep
vep_choices = request_parser.dbNSFP_choices 



application = Flask(__name__)

api.init_app(application)

# By default, show all endpoints (collapsed)
application.config.SWAGGER_UI_DOC_EXPANSION = 'list'


# Allows app to be run in debug mode
if __name__ == '__main__':
    application.debug = True  # Enable debugging mode
    application.run(host="127.0.0.1", port=5000)  # Specify a host and port fot the app
