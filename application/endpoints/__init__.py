from flask_restx import Api

from .vep import api as ns_vep
from .vr import api as ns_vr
from .vv import api as ns_vv

# Define the API as api
api = Api(version="1.0",
          title="VEP, VV, VR",
          description="### Rest APi incorperating Ensembl Variant Recoder, Variant Effect Predictor and Variant Validator")


api.add_namespace(ns_vep)
api.add_namespace(ns_vr)
api.add_namespace(ns_vv)