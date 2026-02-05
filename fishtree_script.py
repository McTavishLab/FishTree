import requests
import json
import dendropy
from opentree import OT

fi = open("../FishTree/alfaro_fishset/main.csv").readlines()

lin = fi[1:] #skip the header
lii = [line.split(",") for line in lin] #split on commas
ott_ids = [int(item[2]) for item in lii] #grabs all opentree ids


# maps ott ids (formatted as node ids) back to names
translation_dict = {"ott"+item[2]:item[1] for item in lii}

treefile = "alfaro_fishset.tre"
#Get the synthetic tree from OpenTree
output = OT.synth_induced_tree(ott_ids=list(ott_ids),  label_format='name')
output.tree.write(path = treefile, schema = "newick")
output.tree.print_plot(width=100)



## show broken taxa
print("broken taxa:")
print(output.response_dict['broken'])

## Get citations
cites = OT.get_citations(output.response_dict['supporting_studies'])
cite_fi = open("topology_citations.txt","w")
cite_fi.write(cites)
cite_fi.close()


## Get Dated synth tree
url     = 'https://dates.opentreeoflife.org/v4/dates/dated_tree'

## Requires node ids - which for ott ids are just the id + 'ott''
payload = { "node_ids" : list(translation_dict.keys())}

resp = requests.post(url=url, data=json.dumps(payload))

resp_dict = resp.json()

## Somehwat annoyingly, the repsonse always has a 'list' of trees, even where there is only one tree

dated_tree = dendropy.Tree.get(string = resp_dict['dated_trees_newick_list'][0], schema="newick")

#The dated tree labels are all as ottids - which are convenient for data analysis but annoying for interpretability

## This uses an API call to translate them back to 
for taxon in dated_tree.taxon_namespace:
    ottid = taxon.label
    taxon.label =  translation_dict[ottid] + "_" + ottid


dated_tree.write(path="labelled_dated_fish.tre", schema="newick")


## Pull the citations for the dates
date_cites = OT.get_citations(resp_dict['date_sources'])
date_cite_fi = open("date_citations.txt","w")
date_cite_fi.write(date_cites)
date_cite_fi.close()



