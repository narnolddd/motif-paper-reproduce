import raphtory as rp
from raphtory.algorithms import local_temporal_three_node_motifs
import pandas as pd

delta = 86400
g = rp.Graph.load_from_file("/Users/naomiarnold/CODE/Raphtory/motifs-reproduce/graph_files/nfts.rp")
print(g)

motifs = rp.algorithms.local_temporal_three_node_motifs(g,delta=delta)

df = pd.DataFrame.from_dict(motifs,orient='index')
df.columns = list(range(1,41))
df['degree'] = df.index.to_series().apply(lambda id: g.node(id).degree())
df['in'] = df.index.to_series().apply(lambda id: g.node(id).in_degree())
df['out'] = df.index.to_series().apply(lambda id: g.node(id).out_degree())
df['transactions'] = df.index.to_series().apply(lambda id: g.node(id).edges.explode().count())

df.to_csv("output_data/nft-local-"+str(delta)+".csv")