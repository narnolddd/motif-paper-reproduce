import raphtory as rp
import pandas as pd
import numpy as np

deltas = range(3600,691200 + 3600,3600)

df = pd.read_csv("/Users/naomiarnold/CODE/Data/NFTs/Data_API_reduced.csv",usecols=[3,5,13],header=0, parse_dates=[2])
df["Datetime_updated_seconds"]=df["Datetime_updated_seconds"].apply(lambda t: int(t.timestamp()))

from raphtory.nullmodels import permuted_timestamps_model

motifs_shuffled_timestamps = []

for i in range(10):
    print("experiment "+str(i))
    permuted_timestamps_model(df,time_name="Datetime_updated_seconds", inplace=True, sorted=True)

    print("building graph")
    g = rp.Graph()
    g.load_edges_from_pandas(df,src="Buyer_address",dst="Seller_address",time="Datetime_updated_seconds")
    print("running motifs")
    motifs = rp.algorithms.global_temporal_three_node_motif_multi(g,deltas=deltas)

    data = [[i] + [deltas[j]] + row for (j,row) in enumerate(motifs)]
    motifs_shuffled_timestamps += data

pd.DataFrame(motifs_shuffled_timestamps).to_csv("output_data/nft_shuffled_time_multi_delta.csv", index=False, header=["experiment", "delta"]+list(map(str,range(40))))