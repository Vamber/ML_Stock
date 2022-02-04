

from Experts.expert_template import expert_template 
from datetime import date 



##
##
##  if you want to add another expert, please also update /Expert/expert_main.py and 
##                                            and  update /Email/main.py 


class expert_vamber(expert_template):
    name = "expert_vamber"


    def __init__(self):
        super().__init__(expert_vamber.name)



    ## nmp == (nasdaq, ml_model_suffix) pair
    ## so this is the strategy vamber
    ## 1. pick all nmp with prediction as 1 (meaning it is predcted)
    ## 2. after that, all nmp with hist acc more than 0.5
    ## 3. after that, all nmp with hist recall less than 0.6
    ## 4. after that, all nmp with last 10d acc more than 0.6
    ## 5. after that, all nmp with last 10d  recall less than 0.4
    def create_today_stock_selection(self):
        filtered_nmp_lst = self.get_nmp_after_iterative_filtering([1, 0.5, 0.6, 0.6, 0.4])
        today_pick = []
        for nmp in filtered_nmp_lst:
            if nmp[0] != "^IXIC":
                today_pick.append(nmp[0])
        today_pick = list(set(today_pick))
        if len(today_pick) == 0:
            today_pick = ["SOLD_ALL"]
        return today_pick




