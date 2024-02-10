from flask import Flask, make_response
from flask_restx import Api, Resource, reqparse, Namespace
import requests
from utils import request_parser


application = Flask(__name__)
api = Api(app = application)

parser_vv = request_parser.parser_vv_content


vv_space = api.namespace('Variant Validator', description=  '''Validates syntax and parameters of variant descriptions according to HGVS''')

@vv_space.route("/variantvalidator/<string:genome_build>/<string:variant_description>/<string:select_transcripts>")
class VariantValidatorClass(Resource):
    @api.doc(parser=parser_vv)
    @api.expect(parser_vv)     
    def get(self, genome_build, variant_description, select_transcripts):
        '''Validates syntax and parameters of variant descriptions according to HGVS'''
        vv_args = parser_vv.parse_args()
        content_type = vv_args.get('content-type', '')
    
        url = f"http://rest.variantvalidator.org/VariantValidator/variantvalidator/{genome_build}/{variant_description}/{select_transcripts}"
        
        # validation = requests.get(url)
        # content= validation.json()

        # if vv_args['content-type'] == 'application/json':
        #     return vv_representations.application_json(content, 200, None)
                    
        # elif vv_args['content-type'] == 'text/xml':
        #     return vv_representations.xml(content, 200, None)
        # else:
        #     return content
        
        validation = requests.get(url, headers={ "Content-Type" : content_type})
              
        if content_type == 'application/json':
                    content = validation.json()
        elif content_type == 'text/xml'or 'text/javascript':
                content = validation.content
                return make_response(content, 200, {'Content-Type': content_type})
        else:
            return {"note": "No Content-Type selected, so data returned as default application/json"}, 200
        
        return content


