


import pandas as pd

import random 

df = pd.read_csv("/home/vamber/ML_stock/Utils/proxies.csv")

proxies = [ 'http://' + str(i) for i in list(df["ip"]) ]


def get_random_proxy_for_google_news():
    proxies = [ str(i) for i in list(df["ip"]) ]
    random_proxy = random.choice(proxies)
    return {"https": random_proxy, "http": random_proxy}


#the reason why we need this function is because
# stupid google trend API doesn't do auto randomization
# therefore it always pick the IP to use, hence getting block by google

def get_random_lst_of_proxy_for_google_trend():
    return [random.choice(proxies)]
