
from flask_restx import Namespace, Resource
from flask import make_response
import requests
from utils import request_parser, helper_functions


parser_vep = request_parser.parser_vep
vep_choices = request_parser.dbNSFP_choices 
parser_vep = request_parser.parser_vep
vep_choices = request_parser.dbNSFP_choices 

api = Namespace('Variant Effect Predictor', description='Determines the effect of the variant on gene, transcript, protein and regulaotry regions')

@api.route("/vep/<string:species>/hgvs/<string:hgvs_notation>")
@api.param("species", "Enter Species name/alias \n"
           ">   e.g human, homo sapiens\n")
           
@api.param("hgvs_notation", "Enter hgvs_notation \n"
           ">   e.g ENST00000366667:c.803C>T\n")
class VariantEPredictorClass(Resource): 
    @api.doc(parser=parser_vep)
    @api.expect(parser_vep, validate=True)  
    def get(self, species, hgvs_notation):
        
        vep_args = parser_vep.parse_args()
        dbNSFP_choices = vep_args.get('dbNSFP', '')
        content_type = vep_args.get('Content-type', '')
        content_input = 'application/json' or content_type  

        url = f"https://rest.ensembl.org/vep/{species}/hgvs/{hgvs_notation}"
                
      
                
        if dbNSFP_choices:
            options_param = None or ','.join(dbNSFP_choices)
            
            for input in dbNSFP_choices:
                if input not in vep_choices:
                 return {"error": f"Invalid option '{input}'. Choose from Choices listed in the Columns of dbNSFP_variant on website 'https://usf.app.box.com/s/r505gv70i1jpzgt2qwyip12no513ehac'"}, 400
            
            url += f"?dbNSFP={options_param}"
          
        validation = requests.get(url, headers={ "Content-Type" : content_input})
          
        content = validation.json()
        if vep_args['Content-type'] == 'application/json':
                return helper_functions.application_json(content, 200, headers={ "Content-Type" : content_input} )
                           
        elif vep_args['Content-type'] == 'text/xml':
                return helper_functions.text_xml(content, 200, headers={ "Content-Type" : 'text/xml'} )
        else:   
                content = validation.text
                return make_response(content, 200)        
          
             
      