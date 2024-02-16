                  
# Import modules
from flask import make_response
from dicttoxml import dicttoxml


def upper_allele(b):
    '''converts list of string into uppercase'''
    for a in b:
        x = b.upper()
        
        return x

def get_allele_filter(vr_allele, allele_choices, content):
    ''' filters response by allele present'''
    allele_filters = {}
   
    for input in vr_allele:
                  allele = upper_allele(input) 
                  if allele in allele_choices:
                       for item in content:
                         if allele in item:
                            allele_filters[allele] = []
                            allele_filters[allele].append(item[allele])
                            return allele_filters
                         else:
                            return {"error": f"{allele} allele is not present in any variant, please choose another allele or leave blank to return output for all allele present"}, 400
                            
                  elif allele not in allele_choices:
                        return {"error": f"Invalid option '{allele}'. Please Choose from: {allele_choices}"}, 400 



def text_xml(data, code, headers):
    '''changes default datatype pf the response to text/xml'''
    resp = make_response(dicttoxml(data), code)
    resp.headers.extend(headers)
    return resp 

def application_json(data, code, headers):
    '''default data type to application/json'''
    resp = make_response((data), code)
    resp.headers.extend(headers)
    return resp 

