from flask_restx import reqparse
from utils import vep_dbNSFP


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


parser_vep = reqparse.RequestParser()        
parser_vep.add_argument('refseq',
                    type=str,
                    help='***Use RefSeq transcript set to report consequences (human only)? Select True for yes or False for no***',
                    choices=['True', 'False'])
parser_vep.add_argument('dbscSNV',
                    type=str,
                    help='***include Predictions for splicing variants from dbscSNV? Select True to include or False to exclude***',
                    choices=['True', 'False'])
parser_vep.add_argument('variant_class',
                    type=str,
                    help='***Output the Sequence Ontology variant class for the input variant? Select True for yes or False for no***',
                    choices=['True', 'False'],)
parser_vep.add_argument('Conservation',
                    type=str,
                    help='***include conservation score from the Ensembl Compara databases for variant positions in returned data? Select True to include or False to exclude***',
                    choices=['True', 'False'])
parser_vep.add_argument('ccds',
                    type=str,
                    help='***Include CCDS transcript identifiers in returned data? Select True to include or False to exclude***',
                    choices=['True', 'False'])
parser_vep.add_argument('dbNSFP',
                    type=str,
                    help='''A database of pathogenicity predictions for missense variants.\n See list of choices to enter in the section: Columns of dbNSFP_variant on website 'https://usf.app.box.com/s/r505gv70i1jpzgt2qwyip12no513ehac' ***\n
                    *** please enter the name exactly as it is written on website to avoid errors. Can include more than one choice by separating with commas:\n
                    e.g single choice:  REVEL_score \n
                    multiple choices: REVEL_score, chr, alt \n
                    To return all, type: ALL     (note: this fetches a large amount of data per variant!)''',
                    required=False, action='split')
dbNSFP_choices = vep_dbNSFP.choices