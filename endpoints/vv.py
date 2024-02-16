from flask import make_response
from flask_restx import Resource, reqparse, Namespace
import requests
from utils import request_parser, helper_functions




parser_vv = request_parser.parser_vv

api = Namespace('Variant Validator', description=  '''Validates syntax and parameters of variant descriptions according to HGVS''')

@api.route("/variantvalidator/<string:genome_build>/<string:variant_description>/<string:select_transcripts>")
@api.param("select_transcripts", "***'all'***\n"
                                 ">   Return all possible transcripts\n"
                                 "\n***Single***\n"
                                 ">   NM_000093.4\n"
                                 "\n***Multiple***\n"
                                 ">   NM_000093.4|NM_001278074.1|NM_000093.3")
@api.param("variant_description", "***HGVS***\n"
                                  ">   NM_000088.3:c.589G>T\n"
                                  ">   NC_000017.10:g.48275363C>A\n"
                                  ">   NG_007400.1:g.8638G>T\n"
                                  ">   LRG_1:g.8638G>T\n"
                                  ">   LRG_1t1:c.589G>T\n"
                                  "\n***Pseudo-VCF***\n"
                                  ">   17-50198002-C-A\n"
                                  ">   17:50198002:C:A\n"
                                  ">   GRCh38-17-50198002-C-A\n"
                                  ">   GRCh38:17:50198002:C:A\n"
                                  "\n***Hybrid***\n"
                                  ">   chr17:50198002C>A\n "
                                  ">   chr17:50198002C>A(GRCh38)\n"
                                  ">   chr17:g.50198002C>A\n"
                                  ">   chr17:g.50198002C>A(GRCh38)")
@api.param("genome_build", "***Accepted:***\n"
                           ">   GRCh37\n"
                           ">   GRCh38\n"
                           ">   hg19\n"
                           ">   hg38")

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
         
        content = validation.json()
        if vv_args['content-type'] == 'application/json':
                return helper_functions.application_json(content, 200, headers={ "content-Type" : content_input} )
                           
        elif vv_args['content-type'] == 'text/xml':
                return helper_functions.text_xml(content, 200, headers={ "content-Type" : 'text/xml'} )
        else:   
                content = validation.text
                return make_response(content, 200)        
        


