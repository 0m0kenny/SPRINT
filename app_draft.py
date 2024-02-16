from flask import Flask, make_response
from flask_restx import Api, Resource, reqparse, Namespace
import requests
from utils import request_parser, helper_functions
import json

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
        filtered_allele = {}


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
        elif content_input == 'text/xml'or content_type == 'text/javascript':
                content = validation.content
                return make_response(content, 200, {'Content-Type': content_input})
                    
        if vr_allele:
            
            for input in vr_allele: 
                allele = helper_functions.upper_allele(input) 
                
                if allele in allele_choices:                                 
                    for item in content:
                        if allele in item:
                            filtered_allele[allele] = []
                            filtered_allele[allele].append(item[allele])

                            return filtered_allele
                        else:
                            return {"error": f"{allele} allele is not present in any variant, please choose another variant or leave blank to return output for all allele present"}, 400
                            
                elif allele not in allele_choices:
                        return {"error": f"Invalid option '{allele}'. Please Choose from: {allele_choices}"}, 400
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
        content_input = 'application/json' or content_type

        url = f"http://rest.variantvalidator.org/VariantValidator/variantvalidator/{genome_build}/{variant_description}/{select_transcripts}"
        
        
        validation = requests.get(url, headers={ "Content-Type" : content_input})
              
        if content_input == 'application/json':
                    content = validation.json()
        elif content_input == 'text/xml'or content_input == 'text/javascript':
                content = validation.content
                return make_response(content, 200, {'Content-Type': content_input})
                
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
        content_input = 'application/json' or content_type

        url = f"https://rest.ensembl.org/vep/{species}/hgvs/{hgvs_notation}"
        
              
        if dbNSFP_choices:
                options_param = None or ','.join(dbNSFP_choices)
                
                for input in dbNSFP_choices:
                
                        if input not in vep_choices:
                            return {"error": f"Invalid option '{input}'. Choose from choices listed in the Columns of dbNSFP_variant on website 'https://usf.app.box.com/s/r505gv70i1jpzgt2qwyip12no513ehac'"}, 400
                    #return {"error": f"Invalid option '{input}'. Choose from Choices listed in the Columns of dbNSFP_variant on website 'https://usf.app.box.com/s/r505gv70i1jpzgt2qwyip12no513ehac'"}, 400
                        
                url += f"?dbNSFP={options_param}"
      

            
        try:
            validation = requests.get(url, headers={ "Content-Type" : content_input})
            if validation.ok:
                               
            #add code to log actual error
        
          
                    
                if content_input == 'application/json':
                    content = validation.json()
                    #content_dict = json.loads(content)
                elif content_input in ['text/xml', 'text/javascript']:
                    content = validation.content
                    return make_response(content, 200, {'Content-Type': content_input})
                    
                return content
            
                 
        except validation.status_code != 400:
            return {"error": 'something went wrong'}
        
        



hello_space = api.namespace('hello', description='Simple API that returns a greeting')
@hello_space.route("/")
class HelloClass(Resource):
	def get(self):
		return {
			"greeting": "Hello World"
		}         

name_space = api.namespace('name', description='Return a name provided by the user')
@name_space.route('/kenny')
class NameClass(Resource):
    def get(self):
        return {
            "My name is" : 'kenny'
        }


if __name__ == '__main__':
    application.debug = True 
    application.run(host="127.0.0.1", port=5000) 