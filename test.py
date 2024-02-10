from flask import Flask, make_response
from flask_restx import Api, Resource, reqparse, Namespace
import requests
from utils import request_parser


application = Flask(__name__)
api = Api(app = application)

parser_vr = request_parser.parser_vr
vr_choices = request_parser.fields_choices
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

        url = f"https://rest.ensembl.org/variant_recoder/{species}/{id}"
       
        #Validate the options
        for option in options:
            if option not in request_parser.fields_choices:
                return {"error": f"Invalid option '{option}'. Choose from: {vr_choices}"}, 400
        
        if options:
            options_param = ','.join(options)
            url += f"?fields={options_param}"
        
        validation = requests.get(url, headers={ "Content-Type" : content_type})
              
        if content_type == 'application/json':
                    content = validation.json()
        elif content_type == 'text/xml'or 'text/javascript':
                content = validation.content
                return make_response(content, 200, {'Content-Type': content_type})
        else:
            return {"note": "No Content-Type selected, so data returned as default application/json"}, 200
        
        return content
        

        


    

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

        
vep_space = api.namespace('Variant Effect Predictor', description='Determines the effect of the variant on gene, transcript, protein and regulaotry regions')
@vep_space.route("/vep/<string:species>/hgvs/<string:hgvs_notation>")
class VariantEPredictorClass(Resource): 
    @api.doc(parser=parser_vep)
    @api.expect(parser_vep)  
    def get(self, species, hgvs_notation):
        '''Determines the effect of the variant on gene, transcript, protein and regulaotry regions'''
        vep_args = parser_vep.parse_args()
        dbNSFP_choices = vep_args.get('dbNSFP', '')
        content_type = vep_args.get('Content-type', '')

        url = f"https://rest.ensembl.org/vep/{species}/hgvs/{hgvs_notation}"
        
       
        for input in dbNSFP_choices:
            if input not in vep_choices:
                return {"error": f"Invalid option '{input}'. Choose from Choices listed in the Columns of dbNSFP_variant on website 'https://usf.app.box.com/s/r505gv70i1jpzgt2qwyip12no513ehac'"}, 400
        
        if dbNSFP_choices:
            options_param = ','.join(dbNSFP_choices)
            url += f"?dbNSFP={options_param}"
        
        validation = requests.get(url, headers={ "Content-Type" : content_type})
              
        if content_type == 'application/json':
                    content = validation.json()
        elif content_type == 'text/xml'or 'text/javascript':
                content = validation.content
                return make_response(content, 200, {'Content-Type': content_type})
        else:
            return {"note": "No Content-Type selected, so data returned as default application/json"}, 200
        
        return content

          



if __name__ == '__main__':
    application.debug = True 
    application.run(host="127.0.0.1", port=5000) 