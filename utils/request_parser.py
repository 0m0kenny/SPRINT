from flask_restx import reqparse
from utils import vep_dbNSFP


# specify optional arguments passed via the URL 
parser_vr = reqparse.RequestParser()

parser_vr.add_argument('Content-type',
                    type=str,
                    help='***Select data type to be returned***',
                    choices=['application/json', 'text/xml','text/javascript'], location='headers', required=False)      

parser_vr.add_argument("fields", 
                    type=str, 
                    help= '''Select the identifiers/notations to include from the following types:
                                ***id (variant ID), hgvsg (HGVS genomic), hgvsc (HGVS coding), hgvsp (HGVS protein), spdi (SPDI genomic)***''', 
                    action='split')
fields_choices = ('id', 'hgvsg', 'hgvsc', 'hgvsp', 'spdi')
parser_vr.add_argument('variant allele', 
                       type=str,
                       help = '''variant recorder provides data for each variant allele if present:
                                    ***filter output by which variant allele(s) you would like to see 
                                    choose only from (T, A, C, G)''', required=False, 
                                    action='split')
allele_choices = ('T', 'A', 'C', 'G', "a", "t", "c", "g")

parser_vv = reqparse.RequestParser()

parser_vv.add_argument('content-type',
                    type=str,
                    help='***Select the response format***',
                    choices=['application/json', 'text/xml'], required=False)


parser_vep = reqparse.RequestParser()  
parser_vep.add_argument('Content-type',
                    type=str,
                    help='***Select data type to be returned***',
                    choices=['application/json', 'text/xml','text/javascript'], required=False)      
parser_vep.add_argument('refseq',
                    type=str,
                    help='***Use RefSeq transcript set to report consequences (human only)? Select True for yes ***',
                    choices=['True'], required=False)
parser_vep.add_argument('dbscSNV',
                    type=str,
                    help='***Include Predictions for splicing variants from dbscSNV? Select True to include***',
                    choices=['True'], required=False)
parser_vep.add_argument('variant_class',
                    type=str,
                    help='***Output the Sequence Ontology variant class for the input variant? Select True for yes***',
                    choices=['True'], required=False)
parser_vep.add_argument('Conservation',
                    type=str,
                    help='***Include conservation score from the Ensembl Compara databases for variant positions in returned data? Select True to include***',
                    choices=['True'], required=False)
parser_vep.add_argument('ccds',
                    type=str,
                    help='***Include CCDS transcript identifiers in returned data? Select True to include***',
                    choices=['True'],required=False )
parser_vep.add_argument('dbNSFP',
                    type=str,
                    help='''A database of pathogenicity predictions for missense variants.\n See list of choices to enter in the section: Columns of dbNSFP_variant on website 'https://usf.app.box.com/s/r505gv70i1jpzgt2qwyip12no513ehac' ***\n
                    *** Please enter the name exactly as it is written on website to avoid errors. Can include more than one choice by separating with commas:\n
                    e.g single choice:  REVEL_score \n
                    multiple choices: REVEL_score, chr, alt \n
                    To return all, type: ALL     (note: this fetches a large amount of data per variant!)''',
                    required=False, action='split')
dbNSFP_choices = vep_dbNSFP.choices