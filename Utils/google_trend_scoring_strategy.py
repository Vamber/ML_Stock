

#
#  Whenever you see a file is called something like ....strategy.py
#  It is used for turning raw_features into processed features
#  No function in this file can establish socket connection (basicaly, can not use internet)
#
##



#####
#
# The current strategy is to return a popularity score vector (a python list) of the past 7 days
#
# 
####

def compute_google_trend_score_for_keyword_from_dataset(dataset_from_a_particular_date, keyword):
    
    df = dataset_from_a_particular_date

    df["only_day"] = df["date"].apply(lambda s: s.split(" ")[0])
    df = df.groupby("only_day").max()
    return list(df[keyword])



