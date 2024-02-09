from flask import Flask, make_response
from flask_restx import Api, Resource, reqparse, Namespace
import requests
from dicttoxml import dicttoxml
from utils import request_parser



application = Flask(__name__)
api = Api(app = application)

parser_vr = request_parser.parser_vr_fields
vr_choices = request_parser.parser_vr_choices


vr_space = api.namespace('Variant Decoder', description='Translates a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI')

@vr_space.route("/variant_recoder/<string:species>/<string:id>")
#@vr_space.param("Filter Data to be returned", "Select the identifiers/notations to include from the following types:\n"
                                # "id (variant ID), hgvsg (HGVS genomic), hgvsc (HGVS coding), hgvsp (HGVS protein), spdi (SPDI genomic)\n", 
                                # "can enter more than one identifers/notations (separate with comma)\n"
                                # ">  e.g id, hgvsg, spdi"
                                # "leave empty to return all")
#@vr_space.param("id", "Enter Species name/alias\n"
           #">   e.g human, homo sapiens\n")
#vr_space.param("Identifier", "Enter Variant Description\n"
#            ">  Can be Variant ID, HGVS notation or genomic SPDI notation\n")
class VariantRecorderClass(Resource):
    @api.doc(parser=parser_vr)
    @api.expect(parser_vr)     
    def get(self, species, id):
        '''Translate a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI'''
        vr_args = parser_vr.parse_args()
    
        options = vr_args.get('fields', '')

        url = f"https://rest.ensembl.org/variant_recoder/{species}/{id}"
       
        #Validate the options
        for option in options:
            if option not in request_parser.parser_vr_choices:
                return {"error": f"Invalid option '{option}'. Choose from: {choices}"}, 400
        
        if options:
            options_param = ','.join(options)
            url += f"?fields={options_param}"
        validation =  requests.get(url, headers={"content-Type" : "application/json"})
        
        content = validation.json()
      
        return content
    
if __name__ == '__main__':
    application.debug = True 
    application.run(host="127.0.0.1", port=5000) 