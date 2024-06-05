import raphtory as rp
from raphtory.algorithms import global_temporal_three_node_motif
import pandas as pd

delta = 86400
g = rp.Graph.load_from_file("/Users/naomiarnold/CODE/Raphtory/motifs-reproduce/graph_files/nfts.rp")
print(g)

motifs = [global_temporal_three_node_motif(g,delta)]
pd.DataFrame(motifs).to_csv("output_data/single_run_"+str(delta)+".csv")