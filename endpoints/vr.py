from flask import  make_response
from flask_restx import Resource, Namespace
import requests
from utils import request_parser, helper_functions
from dicttoxml import dicttoxml


parser_vr = request_parser.parser_vr
vr_choices = request_parser.fields_choices
allele_choices = request_parser.allele_choices


api = Namespace('Variant Recoder', description='Translates a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI')

@api.route("/variant_recoder/<string:species>/<string:id>")
@api.param("species", "Enter Species name/alias\n"
           ">   e.g human, homo sapiens\n")
@api.param("id", "Enter Variant Description\n"
           ">  Can be Variant ID, HGVS notation or genomic SPDI notation eg ENST00000366667:c.803C>T\n")
class VariantRecorderClass(Resource):
    @api.doc(parser=parser_vr)
    @api.expect(parser_vr, validate=True)     
    def get(self, species, id):
        vr_args = parser_vr.parse_args()
        options = vr_args.get('fields', '') #access the optional fields parameter from vep
        content_type = vr_args.get('Content-type', '')
        content_input = 'application/json' or content_type #if no content-type chosen by user default will be application/json
        vr_allele = vr_args.get('variant allele', '')
       

        url = f"https://rest.ensembl.org/variant_recoder/{species}/{id}"
       
        #Validate the options
        if options:
            options_param = None or ','.join(options) 
            
            for input in options:
                if input not in request_parser.fields_choices:
                    return {"error": f"Invalid option '{input}'. Choose from: {vr_choices}"}, 400
        
            url += f"?fields={options_param}"
        
        validation = requests.get(url, headers={ "Content-Type" : content_input})
        
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
        

       


