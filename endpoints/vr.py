from flask import  make_response
from flask_restx import Resource, Namespace
import requests
from utils import request_parser



parser_vr = request_parser.parser_vr
vr_choices = request_parser.fields_choices


api = Namespace('Variant Recoder', description='Translates a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI')

@api.route("/variant_recoder/<string:species>/<string:id>")
@api.param("Filter Data to be returned", "Select the identifiers/notations to include from the following types:\n"
                                "id (variant ID), hgvsg (HGVS genomic), hgvsc (HGVS coding), hgvsp (HGVS protein), spdi (SPDI genomic)\n", 
                                "can enter more than one identifers/notations (separate with comma)\n"
                                ">  e.g id, hgvsg, spdi"
                                "leave empty to return all")
@api.param("id", "Enter Species name/alias\n"
           ">   e.g human, homo sapiens\n")
@api.param("Identifier", "Enter Variant Description\n"
           ">  Can be Variant ID, HGVS notation or genomic SPDI notation\n")
class VariantRecorderClass(Resource):
    @api.doc(parser=parser_vr)
    @api.expect(parser_vr, validate=True)     
    def get(self, species, id):
        vr_args = parser_vr.parse_args()
        
        options = vr_args.get('fields', '')
        content_type = vr_args.get('Content-type', '')
        content_input = 'application/json' or content_type

        url = f"https://rest.ensembl.org/variant_recoder/{species}/{id}"
       
        #Validate the options
        if options:
            options_param = None or ','.join(options)
            
            for input in options:
                if input not in request_parser.fields_choices:
                    return {"error": f"Invalid option '{input}'. Choose from: {vr_choices}"}, 400
        
            url += f"?fields={options_param}"
        
        validation = requests.get(url, headers={ "Content-Type" : content_input})
              
              
        if content_input == 'application/json':
                    content = validation.json()
        elif content_input == 'text/xml'or content_input == 'text/javascript':
                content = validation.content
                return make_response(content, 200, {'Content-Type': content_input})
                
        return content