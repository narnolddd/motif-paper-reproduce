import raphtory as rp
import pandas as pd
import numpy as np

df = pd.read_csv("/Users/naomiarnold/CODE/Data/NFTs/Data_API_reduced.csv",usecols=[3,5,13],header=0, parse_dates=[2])
df["Datetime_updated_seconds"]=df["Datetime_updated_seconds"].apply(lambda t: int(t.timestamp()))

no_experiments = 10
motifs = []
for i in range(no_experiments):
    print("experiment "+str(i))
    df = df.sample(frac=1.0)
    print("building graph")
    g = rp.Graph()
    g.load_edges_from_pandas(df,src_col="Buyer_address",dst_col="Seller_address",time_col="Datetime_updated_seconds")
    print("running motifs")
    print(motifs)
    motifs.append( rp.algorithms.global_temporal_three_node_motif(g,3600))

pd.DataFrame(motifs).to_csv("output_data/nft_shuffled_same_timestamps.csv")