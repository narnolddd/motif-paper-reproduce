import pandas as pd
from collections import defaultdict

hasher = defaultdict(lambda : len(hasher))

df = pd.read_csv("/Users/naomiarnold/CODE/Data/NFTs/Data_API_reduced.csv",usecols=[3,5,13],header=0, parse_dates=[2])
df["Datetime_updated_seconds"]=df["Datetime_updated_seconds"].apply(lambda t: int(t.timestamp()))
df["Buyer_address"] = df["Buyer_address"].apply(lambda x: hasher[x])
df["Seller_address"] = df["Seller_address"].apply(lambda x: hasher[x])
df.to_csv("graph_files/nft_dir/nft-simple.txt",sep=" ", columns=["Buyer_address", "Seller_address", "Datetime_updated_seconds"], header=False, index=False)