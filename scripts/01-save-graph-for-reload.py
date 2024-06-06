# Save graph file as a binary to make for very fast reload for other experiments.

import raphtory as rp
import pandas as pd
import pickle

g = rp.Graph()

# NFTs: Download dataset from https://osf.io/wsnzr/
df = pd.read_csv("/Users/naomiarnold/CODE/Data/NFTs/Data_API_reduced.csv",usecols=[3,5,13],header=0, parse_dates=[2])
df["Datetime_updated_seconds"]=df["Datetime_updated_seconds"].apply(lambda t: int(t.timestamp()))

# read into raphtory graph
g.load_edges_from_pandas(df,src="Buyer_address",dst="Seller_address",time="Datetime_updated_seconds")
g.save_to_file("graph_files/nfts.rp") 