from opentree import OT

fi = open("../FishTree/alfaro_fishset/main.csv").readlines()

lin = fi[1:] #skip the header
lii = [line.split(",") for line in lin] #split on commas
ott_id = [int(item[2]) for item in lii] #grabs all opentree ids

treefile = "alfaro_fishset.tre"
#Get the synthetic tree from OpenTree
output = OT.synth_induced_tree(ott_ids=list(ott_id),  label_format='name')
output.tree.write(path = treefile, schema = "newick")
output.tree.print_plot(width=100)