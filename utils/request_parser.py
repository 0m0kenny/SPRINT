from flask_restx import reqparse



# specify optional arguments passed via the URL 
parser_vr_fields = reqparse.RequestParser()

parser_vr_fields.add_argument("fields", 
                    type=str, 
                    help= '''Select the identifiers/notations to include from the following types:
                                id (variant ID), hgvsg (HGVS genomic), hgvsc (HGVS coding), hgvsp (HGVS protein), spdi (SPDI genomic)''', 
                    action='split')
parser_vr_choices = ('id', 'hgvsg', 'hgvsc', 'hgvsp', 'spdi')
parser_vv_content = reqparse.RequestParser()

parser_vv_content.add_argument('content-type',
                    type=str,
                    help='***Select the response format***',
                    choices=['application/json', 'text/xml'])
