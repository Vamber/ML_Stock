

from Experts.expert_template import expert_template 
from datetime import date 



##
##
##  if you want to add another expert, please also update /Expert/expert_main.py and 
##                                            and  update /Email/main.py 


class expert_nasdaq_fellow(expert_template):
    name = "expert_nasdaq_fellow"


    def __init__(self):
        super().__init__(expert_nasdaq_fellow.name)



    ## 
    ## The strategy overall is similar to expert_vamber, with an addition layer of protecton or conservativeness
    ## if the Nasdaq_market is dropping yesterday, then we don't enter today, and just SELL_ALL
    ##
    ## the reason being, generally a market crash is always a sequential days of Nasdaq going down
    ## with this implementation, we can always avoid market crash
    ##
    ## although it would miss out on days in which the market is raising, but this is a safer strategy in the long term
    ## compare to expert Vamber
   
    def create_today_stock_selection(self):
        
        #immediately returns SOLD_ALL if the market was dropping yesterday  
        if self.market_dropped_yesterday():
            return ["SOLD_ALL"]

        filtered_nmp_lst = self.get_nmp_after_iterative_filtering([1, 0.5, 0.6, 0.6, 0.4])
        today_pick = []
        for nmp in filtered_nmp_lst:
            if nmp[0] != "^IXIC":
                today_pick.append(nmp[0])
        today_pick = list(set(today_pick))
        if len(today_pick) == 0:
            today_pick = ["SOLD_ALL"]
        return today_pick

    




