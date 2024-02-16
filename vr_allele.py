from flask import Flask, make_response
from flask_restx import Api, Resource, reqparse, Namespace, representations
import requests
from utils import request_parser, helper_functions, exceptions
from dicttoxml import dicttoxml


application = Flask(__name__)
api = Api(app = application)





parser_vr = request_parser.parser_vr
vr_choices = request_parser.fields_choices
allele_choices = request_parser.allele_choices
parser_vv = request_parser.parser_vv
parser_vep = request_parser.parser_vep
vep_choices = request_parser.dbNSFP_choices 


vr_space = api.namespace('Variant Recoder', description='Translates a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI')

@vr_space.route("/variant_recoder/<string:species>/<string:id>")
class VariantRecorderClass(Resource):
    
    @api.doc(parser=parser_vr)
    @api.expect(parser_vr, validate=True) 
    
       
    def get(self, species, id):
        '''Translate a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI'''
        vr_args = parser_vr.parse_args()
        
        options = vr_args.get('fields', '')
        content_type = vr_args.get('Content-type', '')
        content_input = 'application/json' or content_type
        vr_allele = vr_args.get('variant allele', '')
        allele_filters = {}

    

        url = f"https://rest.ensembl.org/variant_recoder/{species}/{id}"
       
        #Validate the options
        
        if options:
            options_param = None or ','.join(options)
            
            for input in options:
                if input not in vr_choices:
                    return {"error": f"Invalid option '{input}'. Choose from: {vr_choices}"}, 400
        
            url += f"?fields={options_param}"
        
        validation = requests.get(url, headers={ "Content-Type" : content_input})
        
        validation.raise_for_status() 
        
        content = validation.json()
        
        
        @api.representation('text/xml')
        def text_xml(data, code, headers):
                resp = make_response(dicttoxml(data), code)
                resp.headers.extend(headers)
                return resp
        @api.representation('application/json')
        def application_json(data, code, headers):
                resp = make_response((data), code)
                resp.headers.extend(headers)
                return resp 
     

        # Overrides the default response route so that the standard HTML URL can return any specified format
        if vr_args['Content-type'] == 'application/json':
            if vr_allele: 
                #filters response by allele
                response = helper_functions.get_allele_filter(vr_allele, allele_choices, content)
            
                return application_json(response, 200, headers={ "Content-Type" : content_input} )
            else:
                return application_json(content, 200, headers={ "Content-Type" : content_input} )
        
        elif vr_args['Content-type'] == 'text/xml':
            if vr_allele:
                response = helper_functions.get_allele_filter(vr_allele, allele_choices, content)
                return text_xml(response, 200, headers={ "Content-Type" : 'text/xml'} )
            else:
                return text_xml(content, 200, headers={ "Content-Type" : 'text/xml'} )
        else:
            if vr_allele:
                response = helper_functions.get_allele_filter(vr_allele, allele_choices, content)
                text_response = str(response)
                return make_response(text_response, 200)
            else:   
             content = validation.text
             return make_response(content, 200)
        # try:
        #     validation = requests.get(url, headers={ "Content-Type" : content_input}, timeout=0.01)
        #     validation.raise_for_status() 
        # except TimeoutError:
        #     raise exceptions.RequestTimeoutError('Request is taking too long and has timed out')    
       
             


if __name__ == '__main__':
    application.debug = True 
    application.run(host="127.0.0.1", port=5000) 