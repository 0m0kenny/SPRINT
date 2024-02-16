
# import the requests module
import requests
import json

# Create the class
class MyRequests:

    def __init__(self):
        self.url = None
        self.option = None

    # method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.url)
    
    #Same method as above but need to specify content type for variant recoder or else jsondecoder error raised
    def request_vrdata(self):
        
        return requests.get(self.url, params={"fields" : ",".join(self.option)}, headers={ "Content-Type" : "application/json"}) 

    def request_vepdata(self):
        
     return requests.get(self.url, params={"refseq" : 'True', "dbscSNV" : "True", "variant_class" : "True",
                                           "Conservation" : "True", "ccds": "True", "dbNSFP" : "REVEL_score" }, 
                                           headers={ "Content-Type" : "application/json"})         

    # methodS that assembles the url to request data from the  endpoints
    def VariantRecorder(self, species, id, option=None): #allows options to be optional
        '''Translate a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI'''
        self.species = species
        self.id = id
        self.option = option or [] #optional parameters-[] can allow lists of params
        self.url = f"https://rest.ensembl.org/variant_recoder/{species}/{id}/"
       
        return self.request_vrdata()
    
    def VariantValidator(self, genome_build, variant_description, select_transcripts):
        '''Validates syntax and parameters of variant descriptions according to HGVS'''
        self.genome_build = genome_build
        self.variant_description = variant_description #maybe the vv can take description from vr?
        self.select_transcripts = select_transcripts
        
        self.url = f"http://rest.variantvalidator.org/VariantValidator/variantvalidator/{genome_build}/{variant_description}/{select_transcripts}"
        #self.url = '/'.join(['http://rest.variantvalidator.org/variantvalidator', genome_build, variant_description, select_transcripts])
        return self.request_data()
    
    def VariantEPredictor(self, species, hgvs_notation): #allows options to be optional
        '''Determines the effect of the variant on gene, transcript, protein and regulaotry regions'''
        self.species = species
        self.hgvs_notation = hgvs_notation #maybe take from vv after its been validated?
        self.url = f"https://rest.ensembl.org/vep/{species}/hgvs/{hgvs_notation}/"
        
        return self.request_vepdata()

if __name__ == "__main__":
    mrq = MyRequests()
    
    # request the data
#can try to use user input function to ask for species, id, options parameters, genome build, req seq etc
    vr_response = mrq.VariantRecorder('human', 'ENST00000366667:c.803C>T', option=['hgvsg', 'hgvsc', 'hgvsp', 'id', 'spdi'])
    vv_response = mrq.VariantValidator('hg38', 'NM_001384479.1:c.803C>T', 'NM_001384479.1')
    vep_response = mrq.VariantEPredictor('human', 'ENST00000366667:c.803C>T')


    #print the 3 response sections
    print('-\n--------------------------VARIANT RECODER RESULTS-------------------\n')
    # print('\n---------status code-------------\n',  '\n', vr_response.status_code)
    # print('\n----------headers-------------\n','\n', vr_response.headers)
    # print('\n---------text---------------\n','\n', vr_response.text)
    # print('\n-----------json----------\n', '\n', vr_response.json()) #parse json object into dict
    content = vr_response.json()
    print(type(content))
    print(content)
    print(len(content))
    # content_str = json.dumps(content)
    # print(type(content_str))
    # print(content_str)
    # content_dict = json.loads(content_str)
    # print(type(content_dict))
    # print(content_dict)
    # print(content[0]['T']['hgvsp'])

    def get_allele(self, allele):
        self.allele = allele
        allele =  user_input 
        user_input = input("Enter 'T' or 'A': ")
        for item in content:
            if allele in item:
                selected_dict = item[allele]
                print(selected_dict)
                break
        else:
            print("Invalid input. Please enter 'T' or 'A'.")

    print(vr_response.url)
    print('\n-------end of result--------')
    
    
    # #print(vr_response.json())
    # print('\n--------------------------VARIANT VALIDATOR RESULTS---------------\n')
    # print('\n---------status code-------\n','\n', vv_response.status_code)
    # print('\n-------headers--------\n', '\n', vv_response.headers)
    # print('\n---------text---------\n', '\n', vv_response.text)
    # print('\n--------json---------\n', '\n', vv_response.json())
    
    # print(vv_response.url)
    # print('\n-------end of result--------')
 
    # print('\n--------------------------VARIANT E PREDICTOR RESULTS---------------\n')
    # print('\n---------status code-------\n','\n', vep_response.status_code)
    # print('\n-------headers--------\n', '\n', vep_response.headers)
    # print('\n---------text---------\n', '\n', vep_response.text)
    # print('\n--------json---------\n', '\n', vep_response.json())
    # print('\n-------end of result--------')
    # print(vep_response.url)


#https://rest.ensembl.org/vep/human/hgvs/ENST00000366667:c.803C%3ET/?refseq=True&dbscSNV=True&variant_class=True&Conservation=True&ccds=True&dbNSFP=REVEL_score