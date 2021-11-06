


import pandas as pd

import random 

df = pd.read_csv("Utils/proxies.csv")

proxies = [ 'http://' + str(i) for i in list(df["ip"]) ]


def get_random_proxy_for_google_news():
    proxies = [ str(i) for i in list(df["ip"]) ]
    random_proxy = random.choice(proxies)
    return {"https": random_proxy, "http": random_proxy}


