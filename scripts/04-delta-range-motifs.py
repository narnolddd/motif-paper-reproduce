import raphtory as rp
import pandas as pd
import numpy as np

g = rp.Graph.load_from_file("/Users/naomiarnold/CODE/Raphtory/motifs-reproduce/graph_files/nfts.rp")

deltas = range(3600,691200 + 3600,3600)
motifs = rp.algorithms.global_temporal_three_node_motif_multi(g,deltas=deltas)

data = [[deltas[j]] + row for (j,row) in enumerate(motifs)]

pd.DataFrame(data).to_csv("output_data/nft_multi_delta.csv", index=False, header=["delta"]+list(map(str,range(40))))