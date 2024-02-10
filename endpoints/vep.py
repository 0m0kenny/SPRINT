from flask import Flask, make_response
from flask_restx import Api, Resource, reqparse, Namespace
import requests
from utils import request_parser


application = Flask(__name__)
api = Api(app = application)
parser_vep = request_parser.parser_vep
vep_choices = request_parser.dbNSFP_choices 
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