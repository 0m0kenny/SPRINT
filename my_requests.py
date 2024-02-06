
# import the requests module
import requests
import json
import pprint #converts json data into nicer readable format

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
            
    # methodS that assembles the url to request data from the  endpoints
    def VariantRecorder(self, species, id, option=None): #allows options to be optional
        '''Translate a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI'''
        self.species = species
        self.id = id
        self.option = option or [] #optional parameters-[] can allow lists of params
        self.url = f"https://rest.ensembl.org/variant_recoder/{species}/{id}/"
        #self.url = '/'.join(['http://rest.variantvalidator.org/variantvalidator', genome_build, variant_description, select_transcripts])
        return self.request_vrdata()
    
    def VariantValidator(self, genome_build, variant_description, select_transcripts):
        self.genome_build = genome_build
        self.variant_description = variant_description
        self.select_transcripts = select_transcripts
        
        self.url = f"http://rest.variantvalidator.org/VariantValidator/variantvalidator/{genome_build}/{variant_description}/{select_transcripts}"
        #self.url = '/'.join(['http://rest.variantvalidator.org/variantvalidator', genome_build, variant_description, select_transcripts])
        return self.request_data()

if __name__ == "__main__":
    mrq = MyRequests()
    
    # request the data

    vr_response = mrq.VariantRecorder('human', 'ENST00000366667:c.803C>T', option=['hgvsg', 'hgvsc', 'hgvsp'])
    vv_response = mrq.VariantValidator('hg38', 'NM_001384479.1:c.803C>T', 'NM_001384479.1')

    #print the 3 response sections
    print('-\n--------------------------VARIANT RECODER RESULTS-------------------\n')
    print('\n---------status code-------------\n',  '\n', vr_response.status_code)
    print('\n----------headers-------------\n','\n', vr_response.headers)
    print('\n---------text---------------\n','\n', vr_response.text)
    print('\n-----------json----------\n', '\n', vr_response.json()) #parse json object into dict
    
    print('\n-------end of result--------')
    #print(vr_response.json())
    print('\n--------------------------VARIANT VALIDATOR RESULTS---------------\n')
    print('\n---------status code-------\n','\n', vv_response.status_code)
    print('\n-------headers--------\n', '\n', vv_response.headers)
    print('\n---------text---------\n', '\n', vv_response.text)
    print('\n--------json---------\n', '\n', vv_response.json())
    print('\n-------end of result--------')
    vr_dict = vr_response.json()
   #print(vr_dict['hgvsg'])