


import pandas as pd

df = pd.read_csv("Utils/proxies.csv")

proxies = [ 'http://' + str(i) for i in list(df["ip"]) ]


