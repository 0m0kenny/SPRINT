# Assuming you want to extract 'hgvsc', 'hgvsp', and 'hgvsg' for each item in the list
import re
data_list = [{'T': {'spdi': ['NC_000001.11:230710020:G:A'],
                   'input': 'ENST00000366667:c.803C>T',
                   'id': ['rs1228544607'],
                   'hgvsc': ['ENST00000366667.6:c.803C>T', 'ENST00000679684.1:c.803C>T', 'ENST00000679738.1:c.803C>T', 'ENST00000679802.1:c.803C>T', 'ENST00000679854.1:n.1314C>T', 'ENST00000679957.1:c.803C>T', 'ENST00000680041.1:c.803C>T', 'ENST00000680783.1:c.803C>T', 'ENST00000681269.1:c.803C>T', 'ENST00000681347.1:n.1314C>T', 'ENST00000681514.1:c.803C>T', 'ENST00000681772.1:c.803C>T', 'NM_001382817.3:c.803C>T', 'NM_001384479.1:c.803C>T'],
                   'hgvsg': ['NC_000001.11:g.230710021G>A'],
                   'hgvsp': ['ENSP00000355627.5:p.Ala268Val', 'ENSP00000505981.1:p.Ala268Val', 'ENSP00000505063.1:p.Ala268Val', 'ENSP00000505184.1:p.Ala268Val', 'ENSP00000506646.1:p.Ala268Val', 'ENSP00000504866.1:p.Ala268Val', 'ENSP00000506329.1:p.Ala268Val', 'ENSP00000505985.1:p.Ala268Val', 'ENSP00000505963.1:p.Ala268Val', 'ENSP00000505829.1:p.Ala268Val', 'NP_001369746.2:p.Ala268Val', 'NP_001371408.1:p.Ala268Val']}}]

# Extract 'hgvsc', 'hgvsp', and 'hgvsg' for each item in the list
print(type(data_list))
